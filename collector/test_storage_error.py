from storage import save_error


error = {

    "log_id":1,

    "reason":"HTTP status 500",

    "level":"HIGH"

}


save_error(error)


print("error saved")
