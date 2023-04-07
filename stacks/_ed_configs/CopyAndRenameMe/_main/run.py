from ed_helper_publisher.terraform import TFConstructor


def run(stackargs):

    import random

    # instantiate authoring stack
    stack = newStack(stackargs)

    #######################################################
    # define stack arguments
    #######################################################
    #
    # use variables tags to get arguments 
    #
    # example
    #stack.parse.add_required(key="aws_default_region",
    #                         default="eu-west-1",
    #                         tags="tfvar,resource,db,docker",
    #                         types="str")

    # required
    stack.parse.add_required(key="stackarg_1",
                             tags="tfvar,db",
                             default="test1",
                             types="str")

    # optional
    stack.parse.add_optional(key="stackarg_3",
                             default="test3",
                             tags="tfvar",
                             types="str")

    #######################################################
    # connect this stack to the terraform code (execgroup)
    # execgroup would be 
    #######################################################
    #
    # <nickname>:::<repo>::execgroup_name
    # 
    # with specific version
    # <nickname>:::<repo>::execgroup_name:<version>
    #
    #######################################################

    # tf_execgroup alias isn't necessary, but it
    # provides some standardization across tf stacks
    stack.add_execgroup("<user github usernam>:::<this_repo>::ec2_server",
                        "tf_execgroup")

    # example
    #stack.add_execgroup("elasticdev:::aws::ec2_server",
    #                    "tf_execgroup")

    # Add substack
    stack.add_substack('elasticdev:::tf_executor')

    # initialize
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    #######################################################
    # set any additional variables
    #######################################################
    #
    # example
    #stack.set_variable("subnet_id",
    #                   "subnet-35412351",
    #                   tags="tfvar,db",
    #                   types="str")

    #######################################################
    # use the terraform constructor (helper)
    #######################################################
    tf = TFConstructor(stack=stack,
                       execgroup_name=stack.tf_execgroup.name,
                       provider="aws",
                       resource_name=<provide resource_name for database>,
                       resource_type=<provide resource_type for database>,
                       terraform_type=<provide terraform type to parse terraform state file>)

    # example
    #tf = TFConstructor(stack=stack,
    #                   execgroup_name=stack.tf_execgroup.name,
    #                   provider="aws",
    #                   resource_name=stack.hostname,
    #                   resource_type="server",
    #                   terraform_type="aws_instance")

    #######################################################
    # transfer terraform resource keys
    # to database for querying
    #######################################################
    tf.include(keys=<list of keys>)
    #
    # example
    #
    #tf.include(keys=["id",
    #                 "ami",
    #                 "arn",
    #                 "private_dns",
    #                 "private_ip",
    #                 "public_dns",
    #                 "public_ip"])

    #######################################################
    # map database key/values for ease of querying
    #######################################################
    tf.include(maps=<dict of values to map>)
    #
    # example - inserts key "_id" to be same as "id, 
    #           "region" to be the same as "aws_default_region"
    #
    #tf.include(maps={"_id": "id",
    #                 "region": "aws_default_region"})

    #######################################################
    # resource output to show
    # on saas ui output tab
    #######################################################
    tf.output(keys=<list of keys>)
    #
    # example
    #
    #tf.output(keys=["id",
    #                "ami",
    #                "arn",
    #                "private_ip",
    #                "public_ip"])

    #######################################################
    # finalize the tf_executor
    #######################################################
    stack.tf_executor.insert(display=True,
                             **tf.get())

    return stack.get_results()
