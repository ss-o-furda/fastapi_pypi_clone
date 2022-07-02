from typing import List

from services import package_service, user_service
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase


class IndexViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)

        self.package_count: int = 0
        self.release_count: int = 0
        self.user_count: int = 0
        self.packages: List = []

    async def load(self):
        self.package_count: int = await package_service.package_count()
        self.release_count: int = await package_service.release_count()
        self.user_count: int = await user_service.user_count()
        self.packages: List = await package_service.latest_packages(limit=5)
