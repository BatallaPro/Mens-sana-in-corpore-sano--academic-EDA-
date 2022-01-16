import numpy as np
import pandas as pd


# For quick empty list assignment
def mklist(n):
    for i in range(n):
        yield []
        
# To easily add every item to the correct list
def item_to_lists(item, lists):
    for i in range(len(item)):
        lists[i].append(item[i])
        
    return lists
        
# To return the name of an object
def nameof(obj, namespace):
    return [name for name in namespace if namespace[name] is obj][0]

# To flatten a list
### TODO - Use this function in funcs_driver.py
def flatten(t):
    return [item for sublist in t for item in sublist]

# For a better pd.DataFrame visualization
class display(object):
    '''This class was found in 'Python Data Science Handbook' by jakevdp (Jake Vanderplas),
    which you can access though his GitHub repository
    (https://github.com/jakevdp/PythonDataScienceHandbook)'''
    
    template = '''<div style="float: left; padding: 10px;">
                  <p style='font-family:"Courier New", Courier, monospace'>{0}</p>{1}
                  </div>'''
    
    def __init__(self, *args):
        self.args = args
        
    def _repr_html_(self):
        return '\n'.join(self.template.format(a, eval(a)._repr_html_()) for a in self.args)
    
    def __repr__(self):
        return '\n\n'.join(a + '\n' + repr(eval(a)) for a in self.args)
    
# To store recipes
def recipe(foods):
    searching = True
    list_of_ingredients = []
    quantities_of_ingredients = []

    # Ask for recipe name
    print('¡A COCINAR!\n')
    recipe_name = input('¿Qué vamos a preparar?:\t')

    # Search for ingredients
    while searching == True:
        ingredient = input('\nIntroduce un alimento para buscar (escribe SALIR para finalizar el proceso):\t')
        
        if ingredient == 'SALIR':
            searching = False
            
        else:
            # To look up in the DataFrame for foods containing `ingredient`
            mask = foods['foodname_ESP'].str.contains(ingredient, case=False, na=False)
            options = list(foods.loc[mask]['foodname_ESP'])
            
            # Show user a numered list of options (ingredients found)
            for num, option in enumerate(options):
                print(num, option)

            # Ask for confirmation of ingredient
            ingredient_num = input('\n¿Te referías a alguno de estos ingredientes?\n' + 
                                   'Introduce el número de índice para aceptar o N para volver a buscar\t')
            
            # Handling exceptions - ingredient_number is not an int
            try:
                is_num_error = int(ingredient_num)
                
            except ValueError:
                print('No se ha añadido el ingrediente, vuelve a intentarlo')
                continue
            
            # Handling exceptions - ingredient_number not eligible
            index_error = int(ingredient_num) not in range(len(options))
                            
            # Handling exceptions - search again
            go_back = ingredient_num == 'N'
            
            if go_back or index_error:
                print('No se ha añadido el ingrediente, vuelve a intentarlo')
                continue
            
            # When ingredient is correctly setted, ask for quantity
            quantity = input(f'\n¿Qué cantidad en gramos de {options[int(ingredient_num)]}, ' +
                             'lleva tu {recipe_name}?\t')
                          
            # Store ingredient and quantity
            ingredient_index = foods.index[foods['foodname_ESP'] == options[int(ingredient_num)]].tolist()
            
            list_of_ingredients.append(ingredient_index)
            quantities_of_ingredients.append(int(quantity))
            
    return (recipe_name, list_of_ingredients, quantities_of_ingredients)

# To get nutritional values of a recipe
def recipe_values(recipe, foods):
    # recipe_name = recipe[0]
    list_of_ingredients = flatten(recipe[1])
    quantities = [float(i/100) for i in recipe[2]]
    nutritional_facts =  foods.columns[2:-1]
    recipe_facts = [0]*32

    count_ing = 0

    for ingredient in list_of_ingredients:
        quantity = quantities[count_ing]
        count_fac = 0

        for fact in nutritional_facts:
            fact_value = foods.iloc[ingredient][fact]
            result = fact_value * quantity
            
            recipe_facts[count_fac] += result

            count_fac += 1
        
        count_ing += 1

    return recipe_facts

# To get average nutritional values of a group
def group_values(group, foods):
    ### TODO        
    return group_facts