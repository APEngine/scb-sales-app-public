from admin_management.views import AuthUser

class UserAuthentication():
    @classmethod
    def verifyUser(cls, userCredentials):
        try:
            authenticatedUser = None
            dataBaseUsers = AuthUser.objects.values()
        except:
            print("Error")

print(UserAuthentication.verifyUser("User"))