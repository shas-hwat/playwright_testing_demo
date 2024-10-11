from playwright.sync_api import APIRequestContext
import logging
import json
from utilities.generate_fake_user import (
    generate_fake_user_data_dict,
    generate_random_phone_number,
)

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestUserAPI:
    all_responses = {}
    base_url = "https://practice.expandtesting.com/notes/api/users"  # Relative path since base URL is set in conftest.py
    user_register = "register"
    user_login = "login"
    user_profile = "profile"
    user_change_password = "change-password"
    user_logout = "logout"

    def create_new_user(self, api_request_context: APIRequestContext):
        # Send POST request to register a new user
        new_user_data = generate_fake_user_data_dict()
        logger.info("New User generate >>> " + f"{new_user_data}")

        # Use the POST method from the request context
        response = api_request_context.post(
            f"{self.base_url}/{self.user_register}",
            data=json.dumps(new_user_data),  # Serialize data to JSON
            headers={
                "Content-Type": "application/json"
            },  # Set the content type to JSON
        )
        response_json = response.json()

        if response.status == 409:
            logger.error("POST Failed, USER already exist")
            try:
                # Assert that the status code is 201 (Created)
                assert "id" in response_json, "Response should contain user ID"
            except AssertionError:
                logger.warning(f"{response_json}")

        if response.status == 201:
            logger.info("POST request Successful")
            # Parse the JSON response
            # Print the response for debugging purposes
            logger.info("POST /users/register response:" + f"{response_json}")
            # Additional assertions (optional)
            assert "id" in response_json["data"], "Response should contain user ID"
            assert (
                response_json["data"]["email"] == new_user_data["email"]
            ), "Email mismatch in response"

        self.all_responses["new_user_data"] = new_user_data
        self.all_responses["new_user_response"] = response_json
        return new_user_data, response_json

    def login(self, api_request_context: APIRequestContext):
        user_data_dic, response_json = self.create_new_user(api_request_context)
        user_email = user_data_dic["email"]
        user_password = user_data_dic["password"]

        login_payload = {"email": user_email, "password": user_password}

        # Use the POST method from the request context
        response = api_request_context.post(
            f"{self.base_url}/{self.user_login}",
            data=json.dumps(login_payload),  # Serialize data to JSON
            headers={
                "Content-Type": "application/json"
            },  # Set the content type to JSON
        )
        response_json = response.json()

        self.all_responses["login_response"] = response_json
        if response.status == 200:
            logger.info(
                "Login Successful!!"
                + "\n RESPONSE RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
            return response_json
        if response.status == 400:
            logger.error(
                "Login Failed!!"
                + "\n Bad Request RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
        if response.status == 401:
            logger.error(
                "Login Failed!!"
                + "\n Unauthorized Request RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
        if response.status == 500:
            logger.error(
                "Login Failed!!"
                + "\n Internal Error Server RETURNED FROM SERVER "
                + f"\n{response_json}"
            )

    # @pytest.mark.skip
    def test_get_user_profile(self, api_request_context: APIRequestContext):
        login_response = self.login(api_request_context)
        auth_token = login_response["data"]["token"]

        # Use the get method from the request context
        response = api_request_context.get(
            f"{self.base_url}/{self.user_profile}", headers={"x-auth-token": auth_token}
        )

        response_json = response.json()
        self.all_responses["profile_response"] = response_json

        if response.status == 200:
            logger.info(
                "Get Profile Request Successful!!"
                + "\n RESPONSE RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
            return response_json
        if response.status == 400:
            logger.error(
                "Profile Request Failed!!"
                + "\n Bad Request RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
        if response.status == 401:
            logger.error(
                "Profile Request Failed!!"
                + "\n Unauthorized Request RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
        if response.status == 500:
            logger.error(
                "Profile Request Failed!!"
                + "\n Internal Error Server RETURNED FROM SERVER "
                + f"\n{response_json}"
            )

    # @pytest.mark.skip
    def test_update_the_profile_info(self, api_request_context: APIRequestContext):
        login_response = self.login(api_request_context)
        auth_token = login_response["data"]["token"]
        profile_patch_payload = {
            "name": "shaya",
            "phone": generate_random_phone_number(),
            "company": "",
        }

        # Use the patch method from the request context
        response = api_request_context.patch(
            f"{self.base_url}/{self.user_profile}",
            data=json.dumps(profile_patch_payload),  # Serialize data to JSON
            headers={"Content-Type": "application/json", "x-auth-token": auth_token},
        )  # Set the content type to JSON

        response_json = response.json()
        self.all_responses["update_profile_response"] = response_json
        if response.status == 200:
            logger.info(
                "Update Profile Request Successful!!"
                + "\n RESPONSE RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
            return response_json

    # @pytest.mark.skip
    def test_update_the_profile_password(self, api_request_context: APIRequestContext):
        login_response = self.login(api_request_context)
        current_password = self.all_responses["new_user_data"]["password"]
        new_password = f"{current_password}" + "123"

        auth_token = login_response["data"]["token"]
        update_profile_password_payload = {
            "currentPassword": current_password,
            "newPassword": new_password,
        }

        # Use the POST method from the request context
        response = api_request_context.post(
            f"{self.base_url}/{self.user_change_password}",
            data=json.dumps(update_profile_password_payload),  # Serialize data to JSON
            headers={"Content-Type": "application/json", "x-auth-token": auth_token},
        )  # Set the content type to JSON

        response_json = response.json()
        assert response_json["message"] == "The password was successfully updated"
        if response.status == 200:
            logger.info(
                "Updated Profile Password Successful!!"
                + "\n RESPONSE RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
            return response_json

    def test_logout_the_user(self, api_request_context: APIRequestContext):
        login_response = self.login(api_request_context)
        auth_token = login_response["data"]["token"]

        # Use the DELETE method from the request context
        response = api_request_context.delete(
            f"{self.base_url}/{self.user_logout}", headers={"x-auth-token": auth_token}
        )

        response_json = response.json()
        assert response_json["message"] == "User has been successfully logged out"
        if response.status == 200:
            logger.info(
                "Logout from the Profile Successfully!!"
                + "\n RESPONSE RETURNED FROM SERVER "
                + f"\n{response_json}"
            )
            return response_json
