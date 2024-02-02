
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer


model_name_or_path = "TheBloke/WizardCoder-Python-34B-V1.0-GPTQ"
print("model loading")
model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                             device_map="auto",
                                             trust_remote_code=False,
                                             revision="main")
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)
print("model loaded")


class InputData(BaseModel):
    prompt: str

def ask_llama(prompt):
    data = InputData(prompt=prompt)
    print("Received prompt:", data.prompt)
    
    prompt_template=f'''Below is an instruction that describes a task. Write a response that appropriately completes the request.

    ### Instruction:
    {prompt}

    ### Response:

    '''

    input_ids = tokenizer(prompt_template, return_tensors='pt').input_ids.cuda()
    output = model.generate(inputs=input_ids, temperature=0.1, do_sample=True, top_p=0.95, top_k=10, max_new_tokens=20)
    decoded_output = tokenizer.decode(output[0])

    
    response_start = decoded_output.find("### Response:") + len("### Response:")
    final_response = decoded_output[response_start:].strip()


    # print("Generated response:", final_response)
    return final_response