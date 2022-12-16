# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path
import json
import logging

logger = logging.getLogger(__name__)

VAULTS_FILE = 'obsidian.json'
VAULTS_PATH = Path(os.getenv('APPDATA'), 'obsidian', VAULTS_FILE)


class obsidian(object):

    def __init__(self):
        self.vault_id, self.vault_path, self.vault_name = self.open_vaults()

    @staticmethod
    def open_vaults():
        with open(VAULTS_PATH, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
            vault_id = [x for x in data['vaults']]
            vault_path = [data['vaults'][vaultID]['path'] for vaultID in data['vaults']]
            vault_name = [str(path).split('\\')[-1] for path in vault_path]

        return vault_id, vault_path, vault_name

    def search_notes(self, keyword):

        keyword=re.escape(keyword)
        notes = []
        for i in range(len( self.vault_path)):
            folder = self.vault_path[i]
            for root, dirs, files in os.walk(folder):
                for file in files:

                    if file.endswith('.md'):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            if re.search(keyword, f.read()):
                                notes.append(
                                    Note(file.replace('.md', ""), self.vault_name[i],
                                        file_path.replace(f'{self.vault_path[i]}\\', ""),
                                        keyword))
        return notes


class Vault(object):
    def __init__(self, name, id, path):
        self.name = name
        self.id = id
        self.path = path


class Note(object):
    def __init__(self, note_title, vault_name, note_path, keywords,socre=1):
        # note title
        self.note_title = note_title
        # note's vault nwame
        self.vault_name = vault_name
        # note's path in vault
        self.note_path = note_path
        # search keywords
        self.keywords = keywords
        # obsidian note open link
        self.open_link = self.open_note()
        # Search accuracy
        self.score=socre

    def open_note(self):
        url = f'open?vault={self.vault_name}&file={self.note_path}'.replace(' ', '%20').replace('/', '%2F').replace(
            '\\', '%2F')
        url = f'obsidian://{url}'
        return url


if __name__ == '__main__':
    ob1 = obsidian()

    notes = ob1.search_notes('测试')
    for note in notes:
        print("note_title:", note.note_title, '\nvault_name:', note.vault_name, '\nkeywords:',
              note.keywords, '\nopen_link', note.open_link)

