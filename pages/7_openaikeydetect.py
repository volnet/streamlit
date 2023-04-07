import streamlit as st
# import openai_secret_manager
import openai
import time

st.title("Is your OpenAI Keys available?")
st.markdown("""
Copy & paste the key list in the textbox.
One line with One Key.
""")

def check_key(key):
    # time.sleep(1)
    # return True, 1, ""
    
    model_names = ""
    try:
        openai.api_key = key
        models = openai.Model.list()
        #cheapest_model = min(models, key=lambda x: x['price']['cost_per_minute'])
        #cheapest_model_id = cheapest_model['id']
        cheapest_model_id = "ada"
        prompt = "Hello,"
        # model_names = ",".join([model.id for model in models.data])
        completions = openai.Completion.create(engine=cheapest_model_id, prompt=prompt, max_tokens=5)
        openai_return = completions.choices[0].text
        if len(openai_return) > 0:
            return True, len(models.data), openai_return, ""
        else:
            return False, 0, "", ""
    except Exception as e:
        return False, 0, "", str(e)



key_input = st.text_area("Type OpenAI Key here.")

if st.button("Detect"):
    keys = [key.strip() for key in key_input.split("\n") if key.strip()]
    
    keys_count = st.empty()
    keys_count.text(f"Total keys count : { len(keys) }")
    latest_iteration = st.empty()

    bar = st.progress(0)
    i = 0
    delta = int(100 / len(keys))

    result = "| KEY | Available | Model Count | Result | Error |\n"
    result += "|-------------|--------------|-------------|-------------|-------------|\n"
    for key in keys:
        i = i + 1
        latest_iteration.text(f'Procressing : {i}/{len(keys)}')

        key = key.strip()
        if(len(key) > 0):
            is_available, model_count, model_names, openai_return, error = check_key(key)
            result += f"| {key} | {is_available} | {model_count} | {openai_return} | {error} |\n"
            if "HTTPSConnectionPool" in error:
                st.write(error)
                break

        if i == len(keys):
            bar.progress(100);
        else:
            bar.progress(i * delta)
    st.markdown(result)

