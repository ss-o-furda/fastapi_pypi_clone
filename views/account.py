import fastapi
from fastapi_chameleon import template
from services import user_service
from starlette import status
from starlette.requests import Request
from viewmodels.account.account_viewmodel import AccountViewModel
from viewmodels.account.login_viewmodel import LoginViewModel
from viewmodels.account.register_viewmodel import RegisterViewModel
from infrastructure import cookie_auth

router = fastapi.APIRouter()


@router.get('/account')
@template()
async def index(request: Request):
    vm = AccountViewModel(request)
    await vm.load()
    return vm.to_dict()


@router.get('/account/register')
@template()
def register(request: Request):  # type: ignore
    vm = RegisterViewModel(request)
    return vm.to_dict()


@router.post('/account/register')
@template()
async def register(request: Request):
    vm = RegisterViewModel(request)

    await vm.load()

    if vm.error:
        return vm.to_dict()

    account = await user_service.create_account(
        vm.name, vm.email, vm.password)  # type: ignore

    response = fastapi.responses.RedirectResponse(
        url='/account', status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(response, account.id)

    return response


@router.get('/account/login')
@template()
def login(request: Request):  # type: ignore
    vm = LoginViewModel(request)
    return vm.to_dict()


@router.post('/account/login')
@template()
async def login(request: Request):
    vm = LoginViewModel(request)
    await vm.load()

    if vm.error:
        return vm.to_dict()

    user = await user_service.login_user(vm.email, vm.password)
    if not user:
        vm.error = "The account does not exist or the password is wrong."
        return vm.to_dict()

    resp = fastapi.responses.RedirectResponse(
        '/account', status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(resp, user.id)

    return resp


@router.get('/account/logout')
def logout():
    response = fastapi.responses.RedirectResponse(
        url='/', status_code=status.HTTP_302_FOUND)
    cookie_auth.logout(response)

    return response
