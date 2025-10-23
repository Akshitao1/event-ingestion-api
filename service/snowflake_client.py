import os

import snowflake.connector

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

def get_private_key(env_key):
    private_key_str = os.getenv(env_key, '').replace(r'\\n', '\n')
    private_key = private_key_str.encode('utf-8')
    p_key = serialization.load_pem_private_key(
        private_key,
        password=None,
        backend=default_backend()
    )
    pkb = p_key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption())
    return pkb


team_tag = os.getenv('SF_TEAM_TAG', 'techops')
team_pod_tag = os.getenv('SF_TEAM_POD_TAG', 'tse')
pipeline_tag = os.getenv('SF_PIPELINE_ADHOC_SCRIPTS_TAG', 'adhoc-scripts')

con = snowflake.connector.connect(
        user='TRACKING_CODE_SSH_USER',
        account=os.getenv('SNOWFLAKE_ACCOUNT'),
        private_key=get_private_key("SNOWFLAKE_PRIVATE_KEY"),
        database='TRACKING',
        schema='MODELLED',
        warehouse='UNITY_WH',
        role='TRACKING_ETL',
        session_parameters={
            'QUERY_TAG': f'{{"team":"{team_tag}","team_pod":"{team_pod_tag}","pipeline":"{pipeline_tag}"}}',
        },
    )

def query_snowflake(query_input_string):
    """Snowflake Connection Module."""
    # print("Connecting...")
    ans = []
    cur = None
    try:
        cur = con.cursor()
        sql = ''' {} '''.format(str(query_input_string))
        cur.execute(sql)

        try:
            try:
                # Use fetchall() instead of fetch_pandas_all() to avoid pandas issues
                results = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                ans = []
                for row in results:
                    row_dict = {}
                    for i, value in enumerate(row):
                        row_dict[columns[i]] = value
                    ans.append(row_dict)
            except Exception as e:
                print("getting exception while fetching details:-{}".format(e))
                ans = []
        except Exception as e:
            pass
    except Exception as e:
        print("Database call failed")
    finally:
        if cur:
            try:
                cur.close()
            except Exception as e:
                print(f"Error closing cursor: {e}")
        # print("cursor closed")
        return ans


if __name__ == '__main__':
    query_snowflake(''' SELECT * FROM INBOUND_JOBS limit 10; ''')