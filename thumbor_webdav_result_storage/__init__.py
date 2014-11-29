#coding: utf-8

from thumbor.result_storages import BaseStorage
from thumbor.utils import logger

from tornado.httpclient import HTTPClient

import hashlib
import os

class Storage(BaseStorage):

  def __init__(self, context):
      BaseStorage.__init__(self, context)

  @property
  def _is_auto_webp(self):
      return self.context.config.AUTO_WEBP and self.context.request.accepts_webp

  def put(self, bytes):
      normalized_path = self.normalize_path(self.context.request.url)
      uri = self.context.config.get('RESULT_STORAGE_WEBDAV_HOST') + normalized_path
      logger.debug("[RESULT_STORAGE] Making PUT request to: %s", uri)
      http_client = HTTPClient()
      response = http_client.fetch(uri, _handle_put_request, method='PUT')
      if response.error:
          logger.error("[RESULT_STORAGE] Error on PUT request: %s", response.error)
          return None
      else:
          logger.debug("[RESULT_STORAGE] Success on PUT request!")
          return None

  def get(self):
      normalized_path = self.normalize_path(self.context.request.url)
      uri = self.context.config.get('RESULT_STORAGE_WEBDAV_HOST') + normalized_path
      logger.debug("[RESULT_STORAGE] Making GET request to: %s", uri)
      http_client = HTTPClient()
      response = http_client.fetch(uri, _handle_get_request)
      if response.error:
          logger.debug("[RESULT_STORAGE] Error on GET request: %s", response.error)
          return None
      else:
          logger.debug("[RESULT_STORAGE] Success on GET request!")
          return response.body

  def normalize_path(self, path):
      root_path = self.context.config.get('RESULT_STORAGE_WEBDAV_ROOT_PATH', default='/')
      path_segments = [path]
      if self._is_auto_webp:
          path_segments.append("webp")
      digest = hashlib.sha1(".".join(path_segments).encode('utf-8')).hexdigest()
      return os.path.join(root_path, digest)
