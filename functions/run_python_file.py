import subprocess
import os

def run_python_file(working_directory, file_path, args=None):
    if args is None:
        args = []
    
    full_path = os.path.join(working_directory, file_path)
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        if not os.path.isfile(abs_full_path):
            return f'Error: File "{file_path}" not found.'

        command = ['python', abs_full_path] + args

        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        stdout_output = result.stdout.strip()
        stderr_output = result.stderr.strip()
        
        output_parts = []
        if stdout_output:
            output_parts.append(f"STDOUT:\n{stdout_output}")
        if stderr_output:
            output_parts.append(f"STDERR:\n{stderr_output}")

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        
        if not output_parts:
            return "No output produced."

        return "\n\n".join(output_parts)

    except FileNotFoundError:
        return f'Error: File "{file_path}" not found.'
    except PermissionError:
        return f'Error: Permission denied to execute "{file_path}".'
    except subprocess.TimeoutExpired:
        return f"Error: The script timed out after 30 seconds."
    except Exception as e:
        return f"Error: executing Python file: {e}"
