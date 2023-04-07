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

def get_models(key):
    model_names = ""
    try:
        openai.api_key = key
        models = openai.Model.list()
        model_names = ",".join([model.id for model in models.data])
        return model_names
    except Exception as e:
        return str(e)

st.markdown("## Detect OpenAI Keys")
key_input = st.text_area("Type OpenAI Key here for detecting:")

if st.button("Detect"):
    keys = [key.strip() for key in key_input.split("\n") if key.strip()]
    
    keys_length = len(keys)
    label_keys_count = st.empty()
    label_keys_count.text(f"Total keys count : { keys_length }")
    if(keys_length > 0):
        latest_iteration = st.empty()

        bar = st.progress(0)
        i = 0
        delta = int(100 / keys_length)

        result_available = "";

        result = "<table><tr><td>KEY</td><td>Available</td><td>Model Count</td><td>Result</td><td>Error</td></tr>"
        for key in keys:
            i = i + 1
            latest_iteration.text(f'Procressing : {i}/{keys_length}')

            if(keys_length > 0):
                is_available, model_count, openai_return, error = check_key(key)
                result += f"<tr><td>{key}</td><td>{is_available}</td><td>{model_count}</td><td>{openai_return}</td><td>{error}</td></tr>"
                if is_available:
                    result_available += f"{key}\n"
                if "HTTPSConnectionPool" in error:
                    st.write(error)
                    break

            if i == keys_length:
                bar.progress(100);
            else:
                bar.progress(i * delta)
        result += "</table>"
        st.markdown(result, unsafe_allow_html=True)
        if len(result_available) > 0:
            st.markdown("### Avaiable Keys")
            st.code(result_available, line_numbers=True)
    else:
        st.write("You must enter some keys.")

st.markdown("## Show models")
key_input2 = st.text_area("Type OpenAI Key here for showing models:")

if st.button("Show Models"):
    keys = [key.strip() for key in key_input2.split("\n") if key.strip()]
    keys_length = len(keys)
    if keys_length > 0 :
        result = "| KEY | Models |\n"
        result += "|-------------|--------------|\n"
        for key in keys:
            if(len(key) > 0):
                result += f"| {key} | { get_models(key) } |\n"
            st.markdown(result)
    else:
        st.write("You must enter some keys.")