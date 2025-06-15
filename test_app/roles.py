from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        'create_user': True,
        'delete_user': True,
        'edit_user': True,
    }

class Editor(AbstractUserRole):
    available_permissions = {
        'edit_user': True,
    }

class Viewer(AbstractUserRole):
    available_permissions = {
        'view_user': True,
    }
