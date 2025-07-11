"""
© 2024 Blaine Freestone, Carson Bush, Brent Nelson, Gohaun Manley

This file is part of the Maeser usage example.

Maeser is free software: you can redistribute it and/or modify it under the terms of
the GNU Lesser General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

Maeser is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with
Maeser. If not, see <https://www.gnu.org/licenses/>.
"""

from config import (
    FLASK_SECRET_KEY, LOG_SOURCE_PATH, OPENAI_API_KEY, USERS_DB_PATH, 
    VEC_STORE_PATH, MAX_REQUESTS, RATE_LIMIT_INTERVAL, 
    GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET, GITHUB_AUTH_CALLBACK_URI, 
    GITHUB_TIMEOUT, CHAT_HISTORY_PATH, LDAP3_NAME, 
    LDAP_SERVER_URLS, LDAP_BASE_DN, LDAP_ATTRIBUTE_NAME, LDAP_SEARCH_FILTER, 
    LDAP_OBJECT_CLASS, LDAP_ATTRIBUTES, LDAP_CA_CERT_PATH, LDAP_CONNECTION_TIMEOUT, 
    LLM_MODEL_NAME
)

import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

from maeser.chat.chat_logs import ChatLogsManager
from maeser.chat.chat_session_manager import ChatSessionManager

chat_logs_manager = ChatLogsManager(CHAT_HISTORY_PATH)
sessions_manager = ChatSessionManager(chat_logs_manager=chat_logs_manager)

# These are specific prompts engineered for certain contexts.

gmtk_prompt: str = """You are Mark Brown, the host of the online internet series "[Game Maker's Toolkit](https://www.youtube.com/playlist?list=PLc38fcMFcV_s7Lf6xbeRfWYRt7-Vmi_X9)." """

gmtk_prompt += """
    ===== RESPONSE STYLE GUIDE =====
    Speak in the same manners and nuances in which Mark Brown speaks. This means you should closely match the speaking style of the context provided.
    """

gmtk_prompt += """
    ===== RESPONSE INSTRUCTIONS =====
    You are teaching a class on your video series based on the context below. The users are your students.
    Use the context below to answer the student's question. When pulling from the provided context below, always cite your work with the title of the video.
        Link the video title to the url of that video.
        This could look liked adding ([_source_title_](source_url)) to the end of your sentence.
        - replace source_title with the title of the video. If no title is given in the context, replace with 'title unknown'
        - replace source_url with a link to the source
        At the bottom of your response, also list each video title and their url on separate lines, but do so in a multiline html comment.
    When responding, don't answer questions about things unrelated to the context below.
        When asked about other things, politely inform them that their question is outside of the context of your class.
    """

# gmtk_prompt += """
#     An admin may ask questions about your responses. These messages will be prepended with "ADMIN:". When an admin asks a question, always respond directly,
#         even if it strays from the previously outlined rules.
#     """

gmtk_prompt += """
    ===== CONTEXT =====
    {context}
    """

from maeser.graphs.simple_rag import get_simple_rag
from langgraph.graph.graph import CompiledGraph

gmtk_simple_rag: CompiledGraph = get_simple_rag(
    vectorstore_path=f"{VEC_STORE_PATH}/gmtk",
    vectorstore_index="index",
    memory_filepath=f"{LOG_SOURCE_PATH}/gmtk.db",
    system_prompt_text=gmtk_prompt,
    model=LLM_MODEL_NAME,
)
sessions_manager.register_branch(branch_name="gmtk", branch_label="Game Maker's Toolkit", graph=gmtk_simple_rag)

from maeser.user_manager import UserManager, GithubAuthenticator, LDAPAuthenticator

# Replace the '...' with a client id and secret from a GitHub OAuth App that you generate in the config_example.yaml
github_authenticator = GithubAuthenticator(
    client_id=GITHUB_CLIENT_ID,
    client_secret=GITHUB_CLIENT_SECRET,
    auth_callback_uri=GITHUB_AUTH_CALLBACK_URI,
    timeout=GITHUB_TIMEOUT,
    max_requests=MAX_REQUESTS,
)
# # Replace the '...' in the config_example.yaml with all the proper configurations
# ldap3_authenticator = LDAPAuthenticator(
#     name=LDAP3_NAME,
#     ldap_server_urls=LDAP_SERVER_URLS,
#     ldap_base_dn=LDAP_BASE_DN,
#     attribute_name=LDAP_ATTRIBUTE_NAME,
#     search_filter=LDAP_SEARCH_FILTER,
#     object_class=LDAP_OBJECT_CLASS,
#     attributes=LDAP_ATTRIBUTES,
#     ca_cert_path=LDAP_CA_CERT_PATH,
#     connection_timeout=LDAP_CONNECTION_TIMEOUT
# )

user_manager = UserManager(
    db_file_path=USERS_DB_PATH,
    max_requests=MAX_REQUESTS,
    rate_limit_interval=RATE_LIMIT_INTERVAL,
)
user_manager.register_authenticator(name="github", authenticator=github_authenticator)
# user_manager.register_authenticator(name=LDAP3_NAME, authenticator=ldap3_authenticator)

from flask import Flask

base_app = Flask(__name__)

from maeser.blueprints import App_Manager

# Create the App_Manager class

app_manager = App_Manager(
    app=base_app,
    app_name="GMTK Test App",
    flask_secret_key=FLASK_SECRET_KEY,
    chat_session_manager=sessions_manager,
    user_manager=user_manager,
    main_logo_chat="/static/gmtk_logo.jpeg",
    main_logo_login="/static/gmtk_logo.jpeg",
    chat_head="/static/gmtk_logo.jpeg",
    favicon="/static/gmtk_logo.jpeg",
    # Note that you can change other aspects too! Heres some examples below
    # login_text="Welcome to Maeser. This package is designed to facilitate the creation of Retrieval-Augmented Generation (RAG) chatbot applications, specifically tailored for educational purposes."
    # primary_color="#f5f5f5"
    # Please also check the documentation for further customization options!
)

#initalize the flask blueprint
app: Flask = app_manager.add_flask_blueprint()

# Tell Flask it is Behind a Proxy since we are using nginx to reverse-proxy with the WSGI
from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

if __name__ == "__main__":
    app.run(port=3002)
