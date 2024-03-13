from api.main import app


@app.route("/accounts", methods=['GET'])
def accounts_list():
    return {
        "accounts": []
    }


@app.route("/accounts", methods=['POST'])
def accounts_register():
    return {"name": "accounts post"}


@app.route("/accounts/{account_id}/", methods=['GET'])
def accounts_delete(account_id: str):
    return {
        "id": f"{account_id}",
        "account": "information"
    }


@app.route("/accounts/{account_id}/", methods=['DELETE'])
def accounts_delete(account_id: str):
    return {}