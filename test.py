from core.api.firebase import FirebaseUserManager
from core.api.supabase import MySupabase


supabase=MySupabase()
#test=supabase.sign_up("chakib.elfil2@gmail.com","iamsorry")
test=supabase.login("chakib.elfil2@gmail.com","iamsorry")
print(test)



