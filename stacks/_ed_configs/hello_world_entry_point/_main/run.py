def run(stackargs):

    import json

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="var1")
    stack.parse.add_required(key="var2")

    # hashes that needed to be convered by _BuildSpec class
    stack.parse.add_optional(key="var3",default='null')
    stack.parse.add_optional(key="var4",default='null')

    # Add execgroup
    stack.add_execgroup("elasticdev:::<this repo>::hello_world_group")
    stack.add_substack('elasticdev:::ed_core::publish_resource')

    # Initialize Variables in stack
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    stack.set_variable("stateful_id",stack.random_id())
    stack.set_variable("provider","ed")

    env_vars = { "CLOBBER": True }

    inputargs = {"display":True}
    inputargs["env_vars"] = json.dumps(env_vars)
    inputargs["name"] = 'test hello world'
    inputargs["stateful_id"] = stack.stateful_id
    inputargs["human_description"] = "Creating resource"
    inputargs["display_hash"] = stack.get_hash_object(inputargs)

    stack.hello_world_group.insert(**inputargs)

    if not stack.publish_to_saas: 
        return stack.get_results()

    # publish the info
    keys_to_publish = [ "name",
                        "id",
                        "resource_type" ]

    overide_values = { "name":stack.key_name }
    default_values = { "resource_type":stack.resource_type }
    default_values["publish_keys"] = stack.b64_encode(keys_to_publish)

    inputargs = { "default_values":default_values,
                  "overide_values":overide_values }

    inputargs["automation_phase"] = "infrastructure"
    inputargs["human_description"] = "Publish resource info for hello world"
    stack.publish_resource.insert(display=True,**inputargs)

    return stack.get_results()
