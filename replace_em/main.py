import os
import sys
import time

try:
    from rich.progress import track
    from rich import print as rprint

except ImportError:
    print()
    print("\033[0;31m::\033[0m Missing Dependencies. Please run 'pip3 install -r requirements.txt' before running this script.")
    print()
    sys.exit(1)

INPUT_FILES_PATH = "input_files"


def print_error(msg):
    rprint(f"[bold red]::[/bold red] {msg}")


def print_info(msg):
    rprint(f"[bold green]::[/bold green] {msg}")


def get_user_input(msg, default=None, isint=False):
    while True:
        print()
        if default is not None:
            msg += f" (default: {default})"
        print_info(msg)
        user_input = input("> ").strip()
        if not user_input:
            if default is None:
                print_error("This field in required. Please input what is asked")
                continue
            else:
                user_input = default

        if isint:
            try:
                user_input = int(user_input)
            except ValueError:
                print_error("This value must be a valid integer")
                continue
        break

    return user_input


def get_user_selection(options):
    while True:
        print()
        print_info("Please Select one/multiple from the following (Use '*' to select all):")
        for i,option in enumerate(options):
            rprint(f"    ([blue]{i + 1}[/blue]) [white]{option}[/white]")
        
        input_txt = input("> ").strip()
        if not input_txt:
            print_error("No option selected.")
            continue
        
        if input_txt == "*":
            output = options
            break

        try:
            selected_nums = [int(i) for i in input_txt.split()]
            output = [options[i-1] for i in selected_nums]
            break

        except Exception:
            print_error("Invalid Selection")
            continue
    
    return output


def generate_files(file_path, file_name, str_replace, start_num, end_num):
    if not os.path.exists(file_path):
        print_error(f"{file_path} does not exist.")
        sys.exit(1)

    output_dir = f"output_{file_name}"
    if os.path.exists(output_dir):
        print_error(f"{output_dir} exists. Please remove it first then run the script again.")
        sys.exit(1)

    os.mkdir(output_dir)

    with open(file_path, "r") as f:
        file_data = f.read()

    for i in track(range(start_num, end_num), description="Creating Desired Files"):
        i_str = str(i)
        with open(os.path.join(output_dir, file_name.replace(str_replace, i_str)), 'w') as f:
            f.write(file_data.replace(str_replace, i_str))
        time.sleep(0.01)



if __name__ == "__main__":
    all_files = os.listdir(INPUT_FILES_PATH)
    if not all_files:
        print_error(f"No file in {INPUT_FILES_PATH}/")
        sys.exit(1)
    
    selected_files = get_user_selection(sorted(all_files))
    str_replace = get_user_input("What string do you want to replace?")

    for file in selected_files:
        if str_replace not in file:
            print_error(f"The string in not present in this file's name: [bold white]{file}[/bold white]")
            sys.exit(1)

    start_num = get_user_input("What number do you want the count to start from?", default="0", isint=True)
    end_num = get_user_input("What number do you want the count to end to?", isint=True)
    selected_files_len = str(len(selected_files))

    for i, file in enumerate(selected_files):
        print()
        print_info(f"({str(i + 1)}/{(selected_files_len)}) Working On: [bold white]{file}[/bold white]")
        generate_files(os.path.join(INPUT_FILES_PATH, file), file, str_replace, start_num, end_num)

    print()
    rprint("[bold white]All Files Generated Successfully[/bold white] 🎉")
    print()









