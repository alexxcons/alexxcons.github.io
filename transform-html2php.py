import re
import argparse

def transform_file(input_file, output_file):
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace the pattern
    pattern = r'<p>(.*?)</p>'
    replacement = r'<p><?php E_("\1") ?></p>'
    content = re.sub(pattern, replacement, content)

    # Replace the pattern
    pattern = r'<h2>(.*?)</h2>'
    replacement = r'<h2><?php E_("\1") ?></h2>'
    content = re.sub(pattern, replacement, content)

    # Replace the pattern
    pattern = r'<h3>(.*?)</h3>'
    replacement = r'<h3><?php E_("\1") ?></h3>'
    content = re.sub(pattern, replacement, content)

    # Replace the pattern
    pattern = r'<li>(.*?)</li>'
    replacement = r'<li><?php E_("\1") ?></li>'
    content = re.sub(pattern, replacement, content)

    # Write the transformed content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    parser = argparse.ArgumentParser(description='Transform <p>Text</p> to <p><?php E_("Text") ?></p> in a file.')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('output_file', help='Path to the output file')
    args = parser.parse_args()

    try:
        transform_file(args.input_file, args.output_file)
        print(f"Transformation completed. Output written to {args.output_file}")
    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
