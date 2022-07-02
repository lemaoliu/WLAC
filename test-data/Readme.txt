Suppose the test example is 

{
    "src":"安全 理事会 ，",
    "context_type":"prefix",
    "left_context":"The Security",
    "right_context":"",
    "typed_seq":"Coun",
}

Participants need to predict the target word for this example. If the target word is "Council", then participants need to 
send me the following format to me as follows:

{
    "src":"安全 理事会 ，",
    "context_type":"prefix",
    "left_context":"The Security",
    "right_context":"",
    "typed_seq":"Coun",
    "target":"Council"
}
