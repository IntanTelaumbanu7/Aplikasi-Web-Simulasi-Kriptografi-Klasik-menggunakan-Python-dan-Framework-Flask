import math

def mod_inverse(a, m):
    try:
        return pow(a, -1, m)
    except ValueError:
        return None

def process_affine(text, a, b, mode):
    result = ""
    steps = []
    
    if math.gcd(a, 26) != 1:
        return {"result": "Error", "steps": [f"<span class='text-red-500'>Error: 'a' ({a}) and 26 are not coprime. They share a common factor. Please choose a valid 'a' (e.g., 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25).</span>"]}

    a_inv = mod_inverse(a, 26)
    
    steps.append(f"<b>Mode:</b> {'Encryption' if mode == 'encrypt' else 'Decryption'}")
    steps.append(f"<b>Key:</b> a = {a}, b = {b}")
    
    if mode == 'encrypt':
        steps.append("<b>Formula:</b> " + r"\( E(x) = (ax + b) \pmod{26} \)")
    else:
        steps.append(f"<b>Inverse of a (mod 26):</b> {a_inv} " + r"\( ( \text{since } " + f"{a} \\times {a_inv} \\equiv 1 \\pmod{{26}} ) \)")
        steps.append("<b>Formula:</b> " + r"\( D(x) = a^{-1}(x - b) \pmod{26} \)")
    
    steps.append("<br><b>Step-by-step Transformation:</b>")
    table_rows = []
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            x = ord(char) - ascii_offset
            
            if mode == 'encrypt':
                y = (a * x + b) % 26
                formula_str = f"({a}*{x} + {b}) mod 26 = {y}"
            else:
                y = (a_inv * (x - b)) % 26
                formula_str = f"{a_inv}*({x} - {b}) mod 26 = {y}"
                
            new_char = chr(y + ascii_offset)
            result += new_char
            
            table_rows.append(f"<tr><td class='border px-2 py-1'>{char}</td><td class='border px-2 py-1'>{x}</td><td class='border px-2 py-1 text-center font-mono text-xs'>{formula_str}</td><td class='border px-2 py-1 font-bold'>{new_char}</td></tr>")
        else:
            result += char
            table_rows.append(f"<tr><td class='border px-2 py-1'>{char}</td><td class='border px-2 py-1'>-</td><td class='border px-2 py-1 text-center text-gray-500'>(Not a letter)</td><td class='border px-2 py-1 font-bold'>{char}</td></tr>")
            
    if table_rows:
        table_html = """
        <table class='table-auto w-full max-w-md mt-2 mb-4 text-sm'>
            <thead>
                <tr class='bg-gray-100 dark:bg-gray-700'>
                    <th class='border px-2 py-1'>Char</th>
                    <th class='border px-2 py-1'>Val (x)</th>
                    <th class='border px-2 py-1'>Calculation</th>
                    <th class='border px-2 py-1'>Result</th>
                </tr>
            </thead>
            <tbody>
                {}
            </tbody>
        </table>
        """.format("".join(table_rows))
        steps.append(table_html)
        
    steps.append(f"<b>Final Result:</b> <span class='font-mono bg-gray-100 dark:bg-gray-700 p-1 rounded'>{result}</span>")
    
    return {
        "result": result,
        "steps": steps
    }
