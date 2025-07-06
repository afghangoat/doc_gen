import os
import re

# Usage:
# //? Is defining what the file content is used for.
# //- Is struct documentation
# //! Is function/method documentation

# Assuming there are ALWAYS proper content under the comments and they are properly labeled, no empty or missing comments. Missing comments are not that bad, empty ones are.

#Configurable text values
def_value_label="<b>(Default value)</b>"
def_ret_label="<b>Returns:</b>"
def_linked_label="<b>Next linked list element</b>"
def_param_label="<b>Parameters:</b>"
def_no_ret_label="<i>(Has no return value)</i>"
def_no_par_label="<b>(Has no input parameters)</b>"
def_comment_label="Integer";
pointer_label="(Pointer)";
static_var_ids=[]
static_comments=[]

#Hungarian values
'''def_value_label="<b>(Kezdő érték)</b>"
def_ret_label="<b>Kimenet:</b>"
def_linked_label="<b>(A lista következő eleme)</b>"
def_param_label="<b>Paraméterek:</b>"
def_no_ret_label="<b>(Nincs visszatérési értéke)</b>"
def_no_par_label="<b>(Nincsenek függvény paraméterek)</b>"
def_comment_label="TODO";
pointer_label="(Pointer)";
static_var_ids=["int","vector2d","double","player","scoremanager","fontsurface","bulletmanager","asteroidmanager","explosionmanager","mainmenu","context","renderer","renderingcontext","deathscreen","scoremarker","toplistscreen","highscoreman","scoreman","bullet","asteroid","explosion","button"]
static_comments=["Egész szám","2 dimenziós vektor","Egy valós érték","Játékos","A pontszám kezelő","Referencia a betűfelületre","Referencia a lövedékkezelőre","Referencia az aszteroida kezelőre","Referencia a robbanás kezelőre","A főmenü","A rajzoló kontextus","Az SDL renderer","A rajzoló kontextus","A halálképernyő","Referencia a pontszámjelzőre","Referencia a toplista menüjére","A dicsőséglista","Referencia a pontszámkezelőre","Referencia a lövedékre","Referencia az aszteroidára","Referencia a robbanásra","Referencia a gombra"]
'''

def get_return_and_params(func_str):
    # Match the return type, function name, and parameter list
    match = re.match(r'(\w[\w\s\*]+)\s+(\w+)\s*\(([^)]*)\)', func_str)
    
    if not match:
        return None, None
    
    return_type = match.group(1).strip()
    params_str = match.group(3).strip()

    params = [param.strip() for param in params_str.split(',') if param.strip()]

    return return_type, params

def get_cur_comment(par):
    is_pointer=""
    tpar=par.lower()
    if "*" in tpar:
        is_pointer=pointer_label
    iter=0
    for n in static_var_ids:
        if n in tpar:
            return static_comments[iter]+" "+is_pointer;
        iter+=1
    return def_comment_label+" "+is_pointer;
def generate_doc_data(file_path,afile):
    new_comments=""
    in_struct=False
    t_struct_desc=""
    in_void=True
    ret_t=""
    params_t=[]
    cur_comment=""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                
                t_line=""
                
                if in_void==True:
                    t_line=line
                    t_line=t_line.replace(';',':')
                    t_line=t_line.replace('(','(<b>')
                    t_line=t_line.replace(')',')</b>')
                    new_comments+="<hr/><h3>"+t_line+"</h3><br/>"
                    new_comments+=t_struct_desc
                    ret_t,params_t=get_return_and_params(t_line)
                    if ret_t!= None:
                        new_comments+="<br/>"+def_param_label+"<br/>"
                        if len(params_t)==0:
                            new_comments+=def_no_par_label
                        elif params_t[0]=="void":
                            new_comments+=def_no_par_label
                        else:
                            new_comments+="<ol>"
                            
                            for pars in params_t:
                                cur_comment=get_cur_comment(pars);
                                new_comments+="<li><b>"+pars+"</b>:<i>"+cur_comment+"</i></li>"
                                
                            new_comments+="</ol>"
                        new_comments+="<br>"
                        if ret_t=="void":
                            new_comments+=def_no_ret_label
                        else:
                            new_comments+=def_ret_label+" <i>"+ret_t+"</i><br/>"
                    ret_t=""
                    params_t=[]
                    cur_comment=""
                    in_void=False
                    t_struct_desc=""
                    
                if in_struct==True:
                    t_line=line.strip()
                    if t_line=="":
                        continue
                    if "}" in line:
                        in_struct=False
                        new_comments+="</ul><hr/>"
                    else:
                        t_line=line
                        if "{" in line:
                            t_line="<b>"+t_line
                            t_line=t_line.replace('{','</b',1)
                            t_line=t_line.replace('typedef','',1)
                            t_line=t_line.replace('struct','',1)
                            t_line=t_line.replace(':','',1)
                            t_line+="<\b><br/>"
                            new_comments+=t_struct_desc
                            t_struct_desc=""
                        else:
                            t_line="<li>"+t_line
                            if '=' in t_line:
                                t_line=t_line.replace(';',' '+def_value_label,1)
                            elif "next" in t_line:
                                t_line=t_line.replace(';',' '+def_linked_label,1)
                            else:
                                t_line=t_line.replace(';',' ',1)
                                
                            t_line=t_line.replace('=',' ',1)
                            t_line+="</li>"
                        new_comments+=t_line
                
                if "//?" in line:
                    t_line=line
                    t_line=t_line.replace('//?', '<h2>'+str(afile)+"</h2><p> - ")
                    t_line+='</p><hr/><br/>'
                    new_comments+=t_line
                    continue
                    
                elif line.startswith("//-"):
                    t_struct_desc=line
                    t_struct_desc=t_struct_desc.replace('//-', '<i>')
                    t_struct_desc+=":</i><ul>"
                    in_struct=True
                    continue
                    
                elif line.startswith("//!")==True:
                    t_struct_desc=line
                    t_struct_desc=t_struct_desc.replace('//!', '<i>')
                    t_struct_desc+="</i>"
                    in_void=True
                
    except PermissionError:
        print(f"Skipping file: {file_path} (Permission Denied)")
    
    return new_comments

def process_directory(root_dir):
    s_name=input("Documentation project name (name of the project):")
    scans_h_i=input("Create document from header files? (y/n)")
    scans_h=False
    if scans_h_i == "y":
        scans_h= True

    scans_c_i=input("Create document from source .c files? (y/n)")
    scans_c=False
    if scans_c_i == "y":
        scans_c= True

    document_body="<style>h2,h3,li:nth-child(2n),p{background-color:#ddd}b,h1,h2,h3,i,p{font-family:Consolas,Menlo,Monaco,Lucida Console,Liberation Mono,DejaVu Sans Mono,Bitstream Vera Sans Mono,Courier New,monospace,serif}h3{color:#00f}i,li:nth-child(odd){background-color:#eee}li:nth-child(2n){color:#00f}</style><!--Insert this to a html body element | Auto Generated Documentation--><br/><h1>"+s_name+"</h1><br/><hr/>"
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.c') and scans_c==True:
                file_path = os.path.join(root, file)
                document_body += generate_doc_data(file_path,file)
            if file.endswith('.h') and scans_h==True:
                file_path = os.path.join(root, file)
                document_body += generate_doc_data(file_path,file)
            
    
    print("\nOutput documentation body (copy it to a html body):\n"+document_body)

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ")
    process_directory(folder_path)