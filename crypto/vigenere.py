def process_vigenere(text, key, mode):
    import string

    result = ""
    steps = []

    # Bersihkan key
    key = ''.join([c.upper() for c in key if c.isalpha()])
    if not key:
        return {
            "result": "Error",
            "steps": ["<span class='text-red-500 font-bold'>Error: Key must contain at least one letter.</span>"]
        }

    # =========================
    # TABEL VIGENERE CIPHER
    # =========================
    alphabet = string.ascii_uppercase
    vigenere_rows = []

    header = """
    <tr>
        <th class='sticky left-0 z-20 bg-indigo-700 text-white border px-3 py-2'>#</th>
    """

    for ch in alphabet:
        header += f"""
        <th class='bg-indigo-600 text-white border px-3 py-2 text-center font-semibold'>
            {ch}
        </th>
        """
    header += "</tr>"

    for i in range(26):
        row = f"""
        <tr class='hover:bg-blue-50 dark:hover:bg-gray-700 transition'>
            <th class='sticky left-0 z-10 bg-indigo-100 dark:bg-indigo-900 border px-3 py-2 font-bold'>
                {alphabet[i]}
            </th>
        """

        for j in range(26):
            shifted_char = alphabet[(i + j) % 26]
            row += f"""
            <td class='border px-3 py-2 text-center hover:bg-yellow-200 dark:hover:bg-yellow-500 transition'>
                {shifted_char}
            </td>
            """

        row += "</tr>"
        vigenere_rows.append(row)

    vigenere_table_html = f"""
    <div class='my-6'>
        <div class='bg-white dark:bg-gray-800 shadow-xl rounded-2xl overflow-hidden border'>
            <div class='bg-gradient-to-r from-indigo-600 to-blue-500 px-6 py-4'>
                <h2 class='text-2xl font-bold text-white text-center'>🔐 Tabel Vigenère Cipher</h2>
                <p class='text-center text-blue-100 text-sm mt-1'>
                    Gunakan baris = Key, kolom = Plaintext
                </p>
            </div>

            <div class='overflow-x-auto max-h-[500px] overflow-y-auto p-4'>
                <table class='table-auto border-collapse text-sm min-w-max mx-auto'>
                    <thead class='sticky top-0 z-30'>
                        {header}
                    </thead>
                    <tbody>
                        {''.join(vigenere_rows)}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    """

    steps.append(vigenere_table_html)

    # =========================
    # INFO DASAR
    # =========================
    steps.append(f"<b>Mode:</b> {'Encryption' if mode == 'encrypt' else 'Decryption'}")
    steps.append(f"<b>Key:</b> <span class='text-blue-600 font-bold'>{key}</span>")
    steps.append(
        "<b>Formula:</b> " +
        (r"\( E(x) = (P_i + K_i) \pmod{26} \)" if mode == 'encrypt'
         else r"\( D(x) = (C_i - K_i) \pmod{26} \)")
    )

    steps.append("<br><b class='text-lg'>Step-by-step Transformation:</b>")

    # =========================
    # PERHITUNGAN
    # =========================
    table_rows = []
    key_idx = 0
    key_len = len(key)

    for char in text:
        if char.isalpha():
            is_upper = char.isupper()
            p = ord(char.upper()) - 65
            k_char = key[key_idx % key_len]
            k = ord(k_char) - 65

            if mode == 'encrypt':
                y = (p + k) % 26
            else:
                y = (p - k) % 26

            new_char = chr(y + (65 if is_upper else 97))
            result += new_char

            table_rows.append(
                f"""
                <tr class='hover:bg-gray-50 dark:hover:bg-gray-700'>
                    <td class='border px-3 py-2'>{char} ({p})</td>
                    <td class='border px-3 py-2 text-blue-600 font-bold'>{k_char} ({k})</td>
                    <td class='border px-3 py-2 text-center'>→</td>
                    <td class='border px-3 py-2'>{y}</td>
                    <td class='border px-3 py-2 font-bold text-green-600'>{new_char}</td>
                </tr>
                """
            )

            key_idx += 1

        else:
            result += char
            table_rows.append(
                f"""
                <tr>
                    <td class='border px-3 py-2'>{char}</td>
                    <td class='border px-3 py-2'>-</td>
                    <td class='border px-3 py-2 text-center'>Skip</td>
                    <td class='border px-3 py-2'>-</td>
                    <td class='border px-3 py-2 font-bold'>{char}</td>
                </tr>
                """
            )

    # =========================
    # TABEL LANGKAH
    # =========================
    if table_rows:
        detail_table = """
        <div class='bg-white dark:bg-gray-800 shadow-xl rounded-2xl p-4 mt-6 border'>
            <h3 class='text-xl font-bold text-indigo-600 mb-3'>📊 Detail Perhitungan</h3>
            <div class='overflow-x-auto'>
                <table class='table-auto w-full text-sm border-collapse'>
                    <thead>
                        <tr class='bg-indigo-100 dark:bg-indigo-900'>
                            <th class='border px-3 py-2'>Text (Val)</th>
                            <th class='border px-3 py-2'>Key (Val)</th>
                            <th class='border px-3 py-2'></th>
                            <th class='border px-3 py-2'>New Val</th>
                            <th class='border px-3 py-2'>Result</th>
                        </tr>
                    </thead>
                    <tbody>
                        {}
                    </tbody>
                </table>
            </div>
        </div>
        """.format("".join(table_rows))

        steps.append(detail_table)

    # =========================
    # HASIL AKHIR
    # =========================
    steps.append(
        f"""
        <div class='mt-6 p-5 bg-green-100 dark:bg-green-900 rounded-xl shadow text-center'>
            <b class='text-lg'>Final Result:</b><br>
            <span class='font-mono text-2xl font-bold text-green-700 dark:text-green-300'>
                {result}
            </span>
        </div>
        """
    )

    return {
        "result": result,
        "steps": steps
    }