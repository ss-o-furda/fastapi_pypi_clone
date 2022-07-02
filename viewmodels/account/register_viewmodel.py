from typing import Optional
from starlette.requests import Request
from viewmodels.shared.viewmodel import ViewModelBase
from services import user_service


class RegisterViewModel(ViewModelBase):
    def __init__(self, request: Request) -> None:
        super().__init__(request)

        self.name: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load(self):
        form = await self.request.form()
        self.name = form.get('name')
        self.email = form.get('email')
        self.password = form.get('password')

        if not self.name or not self.name.strip():
            self.error = 'Your name is required'
        elif not self.email or not self.email.strip():
            self.error = 'Your email is required'
        elif not self.password or not self.password.strip():
            self.error = 'Your password is required'
        elif await user_service.get_user_by_email(self.email):
            self.errror = 'Already exists'
