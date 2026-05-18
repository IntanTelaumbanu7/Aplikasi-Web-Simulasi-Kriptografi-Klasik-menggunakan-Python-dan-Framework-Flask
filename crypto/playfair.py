def create_playfair_matrix(key):
    key = "".join(
        c.upper()
        for c in key
        if c.isalpha()
    ).replace("J", "I")

    matrix = []
    used = set()

    for char in key:
        if char not in used:
            matrix.append(char)
            used.add(char)

    for i in range(65, 91):

        char = chr(i)

        if char == "J":
            continue

        if char not in used:
            matrix.append(char)
            used.add(char)

    return [
        matrix[i:i+5]
        for i in range(0, 25, 5)
    ]


def find_pos(matrix, char):

    for r, row in enumerate(matrix):
        for c, val in enumerate(row):

            if val == char:
                return r, c

    return -1, -1


def clean_decrypted_text(text):

    cleaned = ""

    i = 0

    while i < len(text):

        # remove inserted X/Q
        if (
            i < len(text) - 2
            and text[i] == text[i + 2]
            and text[i + 1] in ["X", "Q"]
        ):

            cleaned += text[i]
            i += 2

        else:
            cleaned += text[i]
            i += 1

    # remove trailing filler
    if cleaned.endswith("X"):
        cleaned = cleaned[:-1]

    if cleaned.endswith("Q"):
        cleaned = cleaned[:-1]

    return cleaned


def process_playfair(text, key, mode):

    steps = []

    if not any(
        c.isalpha()
        for c in key
    ):
        return {
            "result": "Error",
            "steps": [
                """
                <span class='text-red-500'>
                Error:
                Key harus memiliki
                minimal satu huruf.
                </span>
                """
            ]
        }

    matrix = create_playfair_matrix(
        key
    )

    # ==========================
    # CHARACTER HANDLING
    # ==========================
    handling_notes = []

    if " " in text:
        handling_notes.append(
            "spasi diabaikan"
        )

    if any(
        not c.isalpha()
        and not c.isspace()
        for c in text
    ):
        handling_notes.append(
            "tanda baca tidak diproses"
        )

    steps.append(
        f"""
        <div class='bg-blue-100
        dark:bg-blue-900
        p-3 rounded-lg my-2'>

        <b>Character Handling:</b><br>

        Playfair Cipher
        hanya mengenkripsi
        huruf alfabet (A-Z).

        {', '.join(handling_notes)}.

        Huruf J otomatis
        menjadi I.

        </div>
        """
    )

    # ==========================
    # SHOW MATRIX
    # ==========================
    matrix_html = """
    <table class='table-auto
    border border-gray-400
    text-center text-lg'>
    """

    for row in matrix:

        matrix_html += "<tr>"

        for val in row:

            matrix_html += f"""
            <td class='border
            border-gray-400
            w-8 h-8'>
            {val}
            </td>
            """

        matrix_html += "</tr>"

    matrix_html += "</table>"

    steps.append(
        f"<b>Key:</b> {key}"
    )

    steps.append(
        f"""
        <b>
        Playfair Matrix
        (5x5, I/J combined):
        </b><br><br>

        {matrix_html}
        """
    )

    # ==========================
    # CLEAN INPUT
    # ==========================
    alpha_text = "".join(
        c.upper()
        for c in text
        if c.isalpha()
    ).replace("J", "I")

    bigrams = []

    # ==========================
    # ENCRYPT BIGRAM
    # ==========================
    if mode == "encrypt":

        i = 0

        while i < len(alpha_text):

            a = alpha_text[i]

            if i + 1 < len(alpha_text):
                b = alpha_text[i + 1]

                if a == b:

                    filler = (
                        "X"
                        if a != "X"
                        else "Q"
                    )

                    bigrams.append(
                        (a, filler)
                    )

                    steps.append(
                        f"""
                        <b>Note:</b>

                        Huruf ganda
                        {a}{a}

                        → disisipkan
                        {filler}
                        """
                    )

                    i += 1

                else:
                    bigrams.append(
                        (a, b)
                    )
                    i += 2

            else:

                filler = (
                    "X"
                    if a != "X"
                    else "Q"
                )

                bigrams.append(
                    (a, filler)
                )

                i += 1

    # ==========================
    # DECRYPT BIGRAM
    # ==========================
    else:

        for i in range(
            0,
            len(alpha_text),
            2
        ):

            if i + 1 < len(alpha_text):

                bigrams.append(
                    (
                        alpha_text[i],
                        alpha_text[i + 1]
                    )
                )

    steps.append(
        """
        <br>
        <b>
        Step-by-step
        Transformation:
        </b>
        """
    )

    table_rows = []

    result_alpha = ""

    for a, b in bigrams:

        r1, c1 = find_pos(
            matrix,
            a
        )

        r2, c2 = find_pos(
            matrix,
            b
        )

        # same row
        if r1 == r2:

            if mode == "encrypt":

                na = matrix[
                    r1
                ][(c1 + 1) % 5]

                nb = matrix[
                    r2
                ][(c2 + 1) % 5]

                rule = (
                    "Same Row "
                    "(Shift Right)"
                )

            else:

                na = matrix[
                    r1
                ][(c1 - 1) % 5]

                nb = matrix[
                    r2
                ][(c2 - 1) % 5]

                rule = (
                    "Same Row "
                    "(Shift Left)"
                )

        # same column
        elif c1 == c2:

            if mode == "encrypt":

                na = matrix[
                    (r1 + 1) % 5
                ][c1]

                nb = matrix[
                    (r2 + 1) % 5
                ][c2]

                rule = (
                    "Same Column "
                    "(Shift Down)"
                )

            else:

                na = matrix[
                    (r1 - 1) % 5
                ][c1]

                nb = matrix[
                    (r2 - 1) % 5
                ][c2]

                rule = (
                    "Same Column "
                    "(Shift Up)"
                )

        # rectangle
        else:

            na = matrix[r1][c2]
            nb = matrix[r2][c1]

            rule = (
                "Rectangle "
                "(Swap Corners)"
            )

        result_alpha += na + nb

        table_rows.append(
            f"""
            <tr>
                <td class='border px-2 py-1'>
                {a}{b}
                </td>

                <td class='border px-2 py-1'>
                {rule}
                </td>

                <td class='border px-2 py-1 font-bold'>
                {na}{nb}
                </td>
            </tr>
            """
        )

    # clean decrypt result
    if mode == "decrypt":
        result_alpha = clean_decrypted_text(
            result_alpha
        )

    table_html = """
    <table class='table-auto
    w-full text-sm mt-2'>
    <thead>
        <tr>
            <th class='border px-2 py-1'>
            Bigram
            </th>

            <th class='border px-2 py-1'>
            Rule Applied
            </th>

            <th class='border px-2 py-1'>
            Result
            </th>
        </tr>
    </thead>

    <tbody>
        {}
    </tbody>
    </table>
    """.format(
        "".join(table_rows)
    )

    steps.append(table_html)

    steps.append(
        f"""
        <b>Final Result:</b>

        <span class='font-mono
        bg-gray-100
        dark:bg-gray-700
        p-1 rounded'>
        {result_alpha}
        </span>
        """
    )

    return {
        "result": result_alpha,
        "steps": steps
    }