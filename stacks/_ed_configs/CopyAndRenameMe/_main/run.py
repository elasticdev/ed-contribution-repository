from ed_helper_publisher.terraform import TFConstructor

def run(stackargs):

    #######################################################
    # import standard python libs
    #######################################################
    import random

    #######################################################
    # instantiate authoring stack
    #######################################################
    stack = newStack(stackargs)

    #######################################################
    # define stack arguments
    #######################################################
    #   - required is required
    #   - optional is only included if provided 
    #     (unless there is a default)
    #
    # use variables tags to organized arguments 
    #
    # stack.parse.add_required(key=<variable_name>,
    #                          types=<variable_types>,
    #                          default=<default variable value>,
    #                          tags=<variable tags>)
    #
    # example
    # 
    # - required stack argument key "aws_default_region"
    # - expects a string
    # - default value is "eu-west-1"
    # 
    # - this key is tagged with tfvar and db
    #   - db is the elasticdev resource database 
    #   - the variable(s) with tags "tfvar" and "db"
    #     will inclue aws_default_region and 
    #     environment (if given)

    # required
    stack.parse.add_required(key="aws_default_region",
                             types="str",
                             default="eu-west-1",
                             tags="tfvar,db")

    # optional
    stack.parse.add_optional(key="environment",
                             tags="tfvar",
                             types="str")

    #######################################################
    # define execgroups
    #######################################################
    #
    # connect this stack to terraform code (execgroup)
    # execgroup would be (version is optional)
    #
    # <nickname>:::<repo>::<execgroup_name>:<version>
    # 
    # stack.add_execgroup("<github user>:::<repository>::<group_name>",
    #                     "<alias>")
    #
    # example
    #
    # ADD 
    #    group name             - "ec2_server"
    #    found in repository    - "aws"
    #    authored by            - "elasticdev"
    #    alias for the group    - "tf_execgroup"
    #

    # add tf execgroup (helper)
    stack.add_execgroup("elasticdev:::aws::ec2_server",
                        "tf_execgroup")
   
    #######################################################
    # define substacks
    #######################################################
    #
    # import or add substack to this stack.
    #
    # NOTE: repo is not needed since stacks are first
    # class citizens.  version is optional
    #
    # <nickname>:::<substack>:<version>
    #
    # stack.add_substack("<github user>:::<stack_name>",
    #                     "<alias>")
    #
    # example - this stack performs the terraform execution
    #
    # ADD 
    #    substack               - "tf_executor"
    #    authored by            - "elasticdev"
    #    alias for the group    - "tf_executor"
    #
    stack.add_substack('elasticdev:::tf_executor')

    #######################################################
    # initialize variables in stack namespace
    #######################################################
    stack.init_variables()

    #######################################################
    # initialize execgroups in stack namespace
    #######################################################
    stack.init_execgroups()
    
    #######################################################
    # initialize substacks in stack namespace
    #######################################################
    stack.init_substacks()
    
    #######################################################
    # explicity set variables in stack namespace
    #######################################################
    #
    # stack.set_variable(<variable_name>,
    #                    <variable_value>,
    #                    tags=<variable tags>,
    #                    types=<variable types allowed>)
    #
    # example
    #
    stack.set_variable("subnet_id",
                       "subnet-35412351",
                       tags="tfvar,db",
                       types="str")

    #######################################################
    # use the terraform constructor (HELPER)
    #######################################################
    #
    # tf = TFConstructor(stack=stack,
    #                    execgroup_name=stack.tf_execgroup.name,
    #                    provider=<provider>",
    #                    resource_name=<resource_name for elasticdev database>,
    #                    resource_type=<resource_type for elasticdev database>,
    #                    terraform_type=<terraform_type for parsing terraform state file>)
    #
    # example
    #
    tf = TFConstructor(stack=stack,
                       execgroup_name=stack.tf_execgroup.name,
                       provider="aws",
                       resource_name=stack.hostname,
                       resource_type="server",
                       terraform_type="aws_instance")

    #######################################################
    # TFConstructor
    # transfer terraform resource key(s) 
    # to elasticdev database for querying
    # and serving as values for other 
    # stacks
    #######################################################
    #
    #tf.include(keys=<list of keys>)
    #
    # example - this resource can be queried
    #           and provide the public_ip for something 
    #           like ssh-ing into the machine
    #
    tf.include(keys=["id",
                     "ami",
                     "arn",
                     "private_dns",
                     "private_ip",
                     "public_dns",
                     "public_ip"])

    #######################################################
    # TFConstructor
    # map database key/values for ease of querying
    #######################################################
    #
    #tf.include(maps=<dict of values to map>)
    #
    # example 
    #         - maps/inserts key "_id" to be same as "id, 
    #         - maps/inserts key "region" to be the same 
    #           as "aws_default_region"
    #
    tf.include(maps={"_id": "id",
                     "region": "aws_default_region"})

    #######################################################
    # TFConstructor
    # resource output to show on saas ui output tab
    #######################################################
    #
    #tf.output(keys=<list of keys>)
    #
    # example
    #
    tf.output(keys=["id",
                    "ami",
                    "arn",
                    "private_ip",
                    "public_ip"])


    #######################################################
    # TFConstructor
    # finalize the tf_executor
    #######################################################

    stack.tf_executor.insert(display=True,
                             **tf.get())

    return stack.get_results()
