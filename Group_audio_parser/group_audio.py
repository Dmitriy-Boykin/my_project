from pprint import pprint

import vk

try:
    import settings
except:
    quit('DO COPY settings_default.py to settings.py and set token')


class GroupAudio:
    """
    Parser of audio recordings on the VK group wall
    Python 3.7
    """
    AUDIOS = []
    GROUP_PARS = []

    def __init__(self, token, group_id):
        """

        :param token: access_token
        :param group_id: group id Vk
        """
        self.token = token
        self.group_id = group_id
        self.vk_session = vk.Session(access_token=self.token)
        self.vk_api = vk.API(session=self.vk_session)
        self.vk_group_parser = self.vk_api.wall.get(domain='thsmsc', count=100, v=5.92)
        self.count = self.vk_group_parser['count'] // 100

    def group_parser(self):
        self.GROUP_PARS.append(self.vk_group_parser['items'])
        for i in range(1, self.count + 1):
            try:
                print(i)
                self.GROUP_PARS.append(
                    self.vk_api.wall.get(domain='thsmsc', count=100, offset=i * 100, v=5.92)['items'])
            except TypeError as exc:
                print(exc)
        self.group_data()
        return self.AUDIOS

    def group_data(self):
        data_groups = self.GROUP_PARS
        for number, audio_list in enumerate(data_groups):
            self.audio_add(audio_list)

    def audio_add(self, audio_list):
        for number, value in enumerate(audio_list):
            for key in value.keys():
                if key == 'attachments':
                    for audio in value[key]:
                        if 'audio' in audio.keys():
                            self.AUDIOS.append({audio['audio']['artist']: audio['audio']['title']})


def data_handler(audios):
    """
    Data processor and output to text file
    :param audios: list of audios from object GroupAudio
    """
    for data in audios:
        for key, value in data.items():
            with open(file='group_audio', mode='a', encoding='utf8') as file:
                file.write(f'{key} - {value} \n')


if __name__ == '__main__':
    group = GroupAudio(token=settings.TOKEN,
                       group_id=settings.GROUP_ID)
    audio_list = group.group_parser()
    data_handler(audios=audio_list)
