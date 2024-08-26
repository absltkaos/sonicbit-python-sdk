import logging

from requests import Session

from sonicbit.enums import RemoteDownloadCommand
from sonicbit.error.error import SonicbitError
from sonicbit.types import RemoteTaskList
from sonicbit.types.path_info import PathInfo

logger = logging.getLogger(__name__)


class RemoteDownload:
    session: Session

    def add_remote_download(self, url: str, path: PathInfo) -> bool:
        logger.debug(f"Adding remote download {url} to {path.path}")

        data = {"url": url, "path": path.path}

        reponse = self.session.post(self.url("/remote_download/task/add"), data=data)

        json_data = reponse.json()
        if json_data.get("success", False):
            return True

        error_message = json_data.get("msg")
        if error_message:
            raise SonicbitError(f"Failed to add remote download: {error_message}")

    def list_remote_downloads(self) -> RemoteTaskList:
        logger.debug("Listing remote downloads")

        params = {"action": RemoteDownloadCommand.LIST_REMOTE_DOWNLOADS.value}
        response = self.session.post(
            self.url("/remote_download/task/list"), params=params
        )

        with open("test.json", "w") as f:
            f.write(response.text)

        return RemoteTaskList.from_response(self, response)

    def delete_remote_download(self, id: int) -> bool:
        logger.debug(f"Deleting remote download with id {id}")

        data = {
            "task_id": id,
        }
        response = self.session.post(
            self.url("/remote_download/task/delete"), data=data
        )

        json_data = response.json()
        if json_data.get("success", False):
            return True

        error_message = json_data.get("msg")
        if error_message:
            raise SonicbitError(f"Failed to delete remote download: {error_message}")

        return False