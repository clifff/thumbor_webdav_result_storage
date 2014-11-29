#coding: utf-8

from thumbor.result_storages import BaseStorage
from thumbor.utils import logger

from tornado.httpclient import HTTPClient, HTTPError

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
      uri = self.context.config.get('RESULT_STORAGE_WEBDAV_URI') + normalized_path
      logger.debug("[RESULT_STORAGE] Making PUT request to: %s", uri)
      http_client = HTTPClient()
      try:
          response = http_client.fetch(uri, method='PUT')
          logger.debug("[RESULT_STORAGE] Success on PUT request!")
      except HTTPError as e:
          logger.error("[RESULT_STORAGE] Error on PUT request: %s", e)

  def get(self):
      normalized_path = self.normalize_path(self.context.request.url)
      uri = self.context.config.get('RESULT_STORAGE_WEBDAV_URI') + normalized_path
      logger.debug("[RESULT_STORAGE] Making GET request to: %s", uri)
      http_client = HTTPClient()
      result = None
      try:
          response = http_client.fetch(uri)
          result = response.body
      except HTTPError as e:
          logger.debug("[RESULT_STORAGE] Error on GET request: %s", e)
      http_client.close()
      return result

  def normalize_path(self, path):
      root_path = '/'
      path_segments = [path]
      if self._is_auto_webp:
          path_segments.append("webp")
      digest = hashlib.sha1(".".join(path_segments).encode('utf-8')).hexdigest()
      return os.path.join(root_path, digest)
