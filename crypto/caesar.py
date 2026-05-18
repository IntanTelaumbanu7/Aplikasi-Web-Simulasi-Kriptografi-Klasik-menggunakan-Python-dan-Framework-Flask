def process_caesar(text, key, mode):
    result = ""
    steps = []
    
    steps.append(f"<b>Mode:</b> {'Encryption' if mode == 'encrypt' else 'Decryption'}")
    steps.append(f"<b>Key (Shift):</b> {key}")
    steps.append("<b>Formula:</b> " + (r"\( E(x) = (x + k) \pmod{26} \)" if mode == 'encrypt' else r"\( D(x) = (x - k) \pmod{26} \)"))
    
    steps.append("<br><b>Step-by-step Transformation:</b>")
    table_rows = []
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            x = ord(char) - ascii_offset
            
            if mode == 'encrypt':
                y = (x + key) % 26
            else:
                y = (x - key) % 26
                
            new_char = chr(y + ascii_offset)
            result += new_char
            
            table_rows.append(f"<tr><td class='border px-2 py-1'>{char}</td><td class='border px-2 py-1'>{x}</td><td class='border px-2 py-1 text-center'>&rarr;</td><td class='border px-2 py-1'>{y}</td><td class='border px-2 py-1 font-bold'>{new_char}</td></tr>")
        else:
            result += char
            table_rows.append(f"<tr><td class='border px-2 py-1'>{char}</td><td colspan='3' class='border px-2 py-1 text-center text-gray-500'>(Not a letter)</td><td class='border px-2 py-1 font-bold'>{char}</td></tr>")
            
    if table_rows:
        table_html = """
        <table class='table-auto w-full max-w-md mt-2 mb-4 text-sm'>
            <thead>
                <tr class='bg-gray-100 dark:bg-gray-700'>
                    <th class='border px-2 py-1'>Char</th>
                    <th class='border px-2 py-1'>Val (x)</th>
                    <th class='border px-2 py-1'></th>
                    <th class='border px-2 py-1'>New Val</th>
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
