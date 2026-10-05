def carica_da_file(file_path):

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            album = []
            header = file.readline()

            for riga in file:
                riga = riga.strip()
                if riga:
                    campi = [c.strip() for c in riga.split(",")]
                    if len(campi) >= 5:
                        codice, titolo, autore, mese_str, anno_str = campi
                        mese = int(mese_str)
                        anno = int(anno_str)

                        foto = [codice, titolo, autore, mese, anno]

                        anno_trovato = False
                        idx = 0
                        while idx < len(album) and not anno_trovato:
                            blocco_anno = album[idx]
                            if blocco_anno[0] == anno:
                                blocco_anno[1].append(foto)
                                anno_trovato = True
                            idx += 1


                        if not anno_trovato:
                            album.append([anno, [foto]])

            return album

    except (FileNotFoundError, ValueError):
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):

    if mese < 1 or mese > 12:
        return None

    codice_duplicato = False
    i = 0
    while i < len(album) and not codice_duplicato:
        blocco_anno = album[i]
        j = 0
        while j < len(blocco_anno[1]) and not codice_duplicato:
            foto = blocco_anno[1][j]
            if foto[0] == codice:
                codice_duplicato = True
            j += 1
        i += 1

    if codice_duplicato:
        return None

    nuova_foto = [codice, titolo, autore, mese, anno]

    try:
        with open(file_path, "a", encoding="utf-8") as file:
            file.write(f"\n{codice},{titolo},{autore},{mese},{anno}")
    except FileNotFoundError:
        return None

    anno_trovato = False
    idx = 0
    while idx < len(album) and not anno_trovato:
        blocco_anno = album[idx]
        if blocco_anno[0] == anno:
            blocco_anno[1].append(nuova_foto)
            anno_trovato = True
        idx += 1

    if not anno_trovato:
        album.append([anno, [nuova_foto]])

    return nuova_foto


def cerca_foto(album, codice):

    risultato = None
    trovato = False
    i = 0
    while i < len(album) and not trovato:
        blocco_anno = album[i]
        j = 0
        while j < len(blocco_anno[1]) and not trovato:
            foto = blocco_anno[1][j]
            if foto[0] == codice:
                risultato = f"{foto[0]}, {foto[1]}, {foto[2]}, {foto[3]}, {foto[4]}"
                trovato = True
            j += 1
        i += 1

    return risultato


def elenco_foto_anno_per_titolo(album, anno):

    titoli = None
    trovato = False
    idx = 0
    while idx < len(album) and not trovato:
        blocco_anno = album[idx]
        if blocco_anno[0] == anno:
            titoli = [foto[1] for foto in blocco_anno[1]]
            titoli.sort()
            trovato = True
        idx += 1

    return titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
