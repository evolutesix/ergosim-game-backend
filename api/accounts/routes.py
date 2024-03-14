from api.main import app


@app.route("/accounts", methods=['GET'])
def account_list():
    return {
        "account": []
    }


@app.route("/accounts", methods=['POST'])
def account_register():
    return {"name": "account post"}


@app.route("/accounts/{account_id}/", methods=['GET'])
def account_details(account_id: str):
    return {
        "id": f"{account_id}",
        "account": "information"
    }


@app.route("/accounts/{account_id}/", methods=['DELETE'])
def account_delete(account_id: str):
    return {}