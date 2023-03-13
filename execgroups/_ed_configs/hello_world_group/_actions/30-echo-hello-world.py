def default():
    
    task = {}
    env_vars = []
    shelloutconfigs = []
    shelloutconfigs.append('elasticdev:::<this repo>::hello_world_shell_script')

    task['method'] = 'shelloutconfig'
    task['metadata'] = {'env_vars': env_vars,
                        'shelloutconfigs': shelloutconfigs
                        }

    return task
