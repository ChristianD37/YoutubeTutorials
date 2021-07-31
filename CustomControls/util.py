import os, json, pygame

def load_existing_save(savefile):
    with open(os.path.join(savefile), 'r+') as file:
        controls = json.load(file)
    return controls

def write_save(data):
    with open(os.path.join(os.getcwd(),'save.json'), 'w') as file:
        json.dump(data, file)

def load_save():
    try:
    # Save is loaded 
        save = load_existing_save('save.json')
    except:
    # No save file, so create one
        save = create_save()
        write_save(save)
    return save


def create_save():
    new_save = {
    "controls":{
        "0" :{"Left": pygame.K_a, "Right": pygame.K_d, "Up": pygame.K_w, "Down": pygame.K_s, 
            "Start": pygame.K_RETURN, "Action1": pygame.K_SPACE},
        "1" :{"Left": pygame.K_a, "Right": pygame.K_d, "Up": pygame.K_w, "Down": pygame.K_s, 
            "Start": pygame.K_RETURN, "Action1": pygame.K_SPACE}
        },
    "current_profile": 0
    }

    return new_save

def reset_keys(actions):
    for action in actions:
        actions[action] = False
    return actions