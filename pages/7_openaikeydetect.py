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
    
    try:
        openai.api_key = key
        models = openai.Model.list()
        #cheapest_model = min(models, key=lambda x: x['price']['cost_per_minute'])
        #cheapest_model_id = cheapest_model['id']
        cheapest_model_id = models.data[0].id
        prompt = "Hello, world."
        models_name = ",".join(models)
        completions = openai.Completion.create(engine=cheapest_model_id, prompt=prompt, max_tokens=5)
        st.write(completions.choices[0].text)
        if completions.choices[0].text == "Hello":
            return True, 1, models_name
        else:
            return False, 0, "No models can use."
    except Exception as e:
        return False, 0, str(e)



key_input = st.text_area("Type OpenAI Key here.")

if st.button("Detect"):
    keys = [key.strip() for key in key_input.split("\n") if key.strip()]
    
    keys_count = st.empty()
    keys_count.text(f"Total keys count : { len(keys) }")
    latest_iteration = st.empty()

    bar = st.progress(0)
    i = 0
    delta = int(100 / len(keys))

    result = "| KEY | Available | Model Count | Models/Error |\n"
    result += "|-------------|--------------|-------------|-------------|\n"
    for key in keys:
        i = i + 1
        latest_iteration.text(f'Procressing : {i}/{len(keys)}')

        key = key.strip()
        if(len(key) > 0):
            is_available, model_count, model_names = check_key(key)
            result += f"| {key} | {is_available} | {model_count} | {model_names} |\n"
            if "HTTPSConnectionPool" in model_names:
                st.write(model_names)
                break

        if i == len(keys):
            bar.progress(100);
        else:
            bar.progress(i * delta)
    st.markdown(result)

