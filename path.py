import gcloud.exceptions as gcloudex


class Path:
    def __init__(self, client, path):
        self.client = client
        self._bucket_obj = None
        self._blob_obj = None
        self._exists = None
        self._is_dir = None

        if path.startswith("gs:///"):
            self._walk_path(path[5:])
        elif path.startswith("gs://"):
            self._walk_path(path[4:])
        elif path.startswith('/'):
            self._walk_path(path)
        else:
            self._walk_path(client.cwd.get_path() + '/' + path)

    def _walk_path(self, path):
        dirs = []
        for d in path.strip('/').split('/'):
            if d == '.' or d.strip() == '':
                continue
            elif d == '..':
                if len(dirs) > 0:
                    dirs.pop()
            else:
                dirs.append(d)

        if len(dirs) == 0:
            self.bucket = None
            self.blob = None
        else:
            self.bucket = dirs[0]
            if len(dirs) == 1:
                self.blob = None
            else:
                self.blob = '/'.join(dirs[1:])

    def get_bucket(self):
        if self._bucket_obj is False:
            return None

        if self._bucket_obj is not None:
            return self._bucket_obj

        try:
            b = self.client.get_bucket(self.bucket)
            self._bucket_obj = b
            return b
        except (gcloudex.NotFound, gcloudex.Forbidden, gcloudex.BadRequest):
            self._bucket_obj = False
            return None

    def get_blob(self):
        if not self.exists() or self.is_directory():
            return None

        return self._blob_obj

    def exists(self):
        if self._exists is not None:
            return self._exists

        if self.bucket is None:
            self._exists = True
            self._is_dir = True
            return True

        if self.get_bucket() is None:
            self._exists = False
            return False

        if self.blob is None:
            self._exists = True
            self._is_dir = True
            return True

        # Try file
        self._blob_obj = self._bucket_obj.get_blob(self.blob)
        if self._blob_obj:
            self._exists = True
            self._is_dir = False
            return True
        else:
            # Try directory
            if len(list(self._bucket_obj.list_blobs(
                    prefix=self.blob + '/'))) > 0:
                self._exists = True
                self._is_dir = True
                return True

        return False

    def is_directory(self):
        if not self.exists():
            return False
        return self._is_dir

    def get_path(self):
        s = "/"
        if self.bucket is not None:
            s += self.bucket
            if self.blob is not None:
                s += "/" + self.blob
        return s

    def is_root(self):
        return self.bucket is None

    def is_bucket_root(self):
        return self.bucket is not None and self.blob is None

    def __str__(self):
        return "gs://" + self.get_path()

    def __repr__(self):
        return "<Path: {}>".format(self.__str__())
