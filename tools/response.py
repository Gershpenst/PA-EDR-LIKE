import json

def bodyMessageError(error):
    return {"success": False, "message_error": error}

def bodyMessageValid(body):
    return {"success": True, "body": body}