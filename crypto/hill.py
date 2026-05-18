import numpy as np


def mod_inverse(a, m):
    a = a % m

    for x in range(1, m):
        if (a * x) % m == 1:
            return x

    return None


def create_matrix_html(matrix):
    html = """
    <table class='inline-block border-l-2 border-r-2
    border-gray-800 dark:border-gray-200
    text-center mx-2'>
    """

    for row in matrix:
        html += "<tr>"

        for val in row:
            html += f"""
            <td class='px-2 py-1'>
                {int(round(val))}
            </td>
            """

        html += "</tr>"

    html += "</table>"

    return html


def process_hill(text, key_matrix, mode):

    steps = []

    key_matrix = np.array(key_matrix)

    # ==================================
    # PREPROCESS TEXT
    # ==================================
    alpha_text = ""

    for char in text:
        if char.isalpha():
            alpha_text += char.upper()

    n = len(key_matrix)

    # ==================================
    # PADDING
    # ==================================
    padding_added = 0

    if len(alpha_text) % n != 0:
        padding_added = n - (
            len(alpha_text) % n
        )

        alpha_text += "X" * padding_added

        steps.append(
            f"""
            <div class='bg-yellow-100
            dark:bg-yellow-900
            p-3 rounded-lg'>

            <b>Note:</b>

            Panjang teks tidak
            sesuai ukuran matriks
            ({n}x{n}).

            Padding ditambahkan:

            <span class='font-mono'>
            {'X' * padding_added}
            </span>

            </div>
            """
        )

    # ==================================
    # SHOW KEY MATRIX
    # ==================================
    matrix_html = create_matrix_html(
        key_matrix
    )

    steps.append(
        f"""
        <div class='bg-blue-50
        dark:bg-gray-800
        p-3 rounded-lg'>

        <b>Key Matrix (K):</b><br>

        {matrix_html}

        </div>
        """
    )

    # ==================================
    # DECRYPTION MODE
    # ==================================
    if mode == "decrypt":

        det = int(
            round(
                np.linalg.det(key_matrix)
            )
        ) % 26

        det_inv = mod_inverse(det, 26)

        if det_inv is None:
            return {
                "result": "Error",
                "steps": [
                    f"""
                    <div class='text-red-500'>

                    Error:

                    Determinant
                    ({det})
                    tidak memiliki
                    inverse modulo 26.

                    Matrix tidak valid
                    untuk Hill Cipher.

                    </div>
                    """
                ]
            }

        # ==================================
        # MANUAL ADJUGATE MATRIX
        # ==================================
        cofactor_matrix = np.zeros(
            (n, n)
        )

        for row in range(n):
            for col in range(n):

                minor = np.delete(
                    np.delete(
                        key_matrix,
                        row,
                        axis=0
                    ),
                    col,
                    axis=1
                )

                cofactor = (
                    (-1) ** (row + col)
                ) * round(
                    np.linalg.det(minor)
                )

                cofactor_matrix[
                    row
                ][col] = cofactor

        # transpose
        adjugate = (
            cofactor_matrix.T
        )

        # inverse modulo 26
        inv_matrix = (
            det_inv *
            adjugate
        ) % 26

        inv_matrix = (
            inv_matrix.astype(int)
        )

        inv_html = create_matrix_html(
            inv_matrix
        )

        steps.append(
            f"""
            <div class='bg-green-50
            dark:bg-gray-800
            p-3 rounded-lg'>

            <b>
            Decryption Process
            </b><br><br>

            <b>
            Determinant:
            </b><br>

            det(K)
            =
            {det}

            <br><br>

            <b>
            Multiplicative
            Inverse:
            </b><br>

            det⁻¹ mod 26
            =
            {det_inv}

            <br><br>

            <b>
            Inverse Matrix
            (K⁻¹ mod 26):
            </b><br>

            {inv_html}

            </div>
            """
        )

        working_matrix = inv_matrix

    else:
        working_matrix = key_matrix

    # ==================================
    # STEP BY STEP
    # ==================================
    steps.append(
        """
        <div class='text-lg
        font-bold mt-4'>

        Step-by-Step
        Matrix Multiplication

        </div>
        """
    )

    result_alpha = ""

    for i in range(
        0,
        len(alpha_text),
        n
    ):

        block = alpha_text[i:i+n]

        vector = np.array(
            [
                ord(c) - 65
                for c in block
            ]
        ).reshape(n, 1)

        # matrix multiplication
        res_vector = np.dot(
            working_matrix,
            vector
        ) % 26

        res_block = "".join(
            chr(
                int(v[0]) + 65
            )
            for v in res_vector
        )

        result_alpha += res_block

        # ==================================
        # VISUAL MATRIX
        # ==================================
        matrix_visual = (
            create_matrix_html(
                working_matrix
            )
        )

        vector_visual = (
            create_matrix_html(
                vector
            )
        )

        result_visual = (
            create_matrix_html(
                res_vector
            )
        )

        # ==================================
        # DETAILED CALCULATION
        # ==================================
        calculation_html = ""

        for row_idx in range(n):

            formula_parts = []
            total = 0

            for col_idx in range(n):

                a = int(
                    working_matrix[
                        row_idx
                    ][col_idx]
                )

                b = int(
                    vector[
                        col_idx
                    ][0]
                )

                formula_parts.append(
                    f"({a} × {b})"
                )

                total += (
                    a * b
                )

            mod_result = (
                total % 26
            )

            result_char = chr(
                mod_result + 65
            )

            calculation_html += f"""
            <div class='bg-gray-100
            dark:bg-gray-700
            rounded p-2 my-2'>

            <b>
            Baris
            {row_idx + 1}
            </b><br>

            {' + '.join(formula_parts)}

            <br>

            = {total}

            <br>

            {total}
            mod 26

            =

            <span class='font-bold'>
            {mod_result}
            </span>

            →

            <span class='font-mono
            font-bold'>
            {result_char}
            </span>

            </div>
            """

        # ==================================
        # STEP HTML
        # ==================================
        step_html = f"""
        <div class='border
        rounded-xl p-4 my-4
        bg-white
        dark:bg-gray-800
        shadow-sm'>

        <div class='mb-3'>

        <b>Block:</b>

        <span class='font-mono
        bg-blue-100
        dark:bg-blue-900
        px-2 py-1 rounded'>

        {block}

        </span>

        </div>

        <div class='flex
        items-center
        flex-wrap
        gap-2 mb-4'>

        {matrix_visual}

        <span class='text-xl'>
        ×
        </span>

        {vector_visual}

        <span class='text-xl'>
        =
        </span>

        {result_visual}

        </div>

        <div>

        <b>
        Detailed Calculation:
        </b>

        {calculation_html}

        </div>

        <div class='mt-3'>

        <b>
        Result Block:
        </b>

        <span class='font-mono
        bg-green-100
        dark:bg-green-900
        px-2 py-1 rounded'>

        {res_block}

        </span>

        </div>

        </div>
        """

        steps.append(step_html)

    # ==================================
    # REBUILD ORIGINAL FORMAT
    # ==================================
    final_result = ""

    alpha_idx = 0

    for char in text:

        if char.isalpha():

            c = result_alpha[
                alpha_idx
            ]

            if char.islower():
                c = c.lower()

            final_result += c

            alpha_idx += 1

        else:
            final_result += char

    # append padding
    while alpha_idx < len(
        result_alpha
    ):
        final_result += (
            result_alpha[
                alpha_idx
            ]
        )

        alpha_idx += 1

    # ==================================
    # FINAL RESULT
    # ==================================
    steps.append(
        f"""
        <div class='bg-green-100
        dark:bg-green-900
        p-4 rounded-xl
        text-lg'>

        <b>
        Final Result:
        </b><br>

        <span class='font-mono
        text-xl'>

        {final_result}

        </span>

        </div>
        """
    )

    return {
        "result": final_result,
        "steps": steps
    }