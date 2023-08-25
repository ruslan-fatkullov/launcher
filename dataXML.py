import xml.etree.ElementTree as ElTree


class DataXML:

    def __init__(self):
        self.root = ElTree.Element("data")

    def add_group(self, group_id, name):
        data_element = ElTree.SubElement(self.root, "board")
        data_element.set("id", str(group_id))
        data_element.set("name", name)
        tree = ElTree.ElementTree(self.root)
        tree.write("data.xml")

    def get_groups(self):
        try:
            self.root.clear()
            tree = ElTree.parse("data.xml")
            self.root.extend(tree.getroot())
        except:
            print("нет групп")

    def remove_group(self, group_name):
        for data_element in self.root.findall("board"):
            if data_element.get("name") == str(group_name):
                self.root.remove(data_element)
                tree = ElTree.ElementTree(self.root)
                tree.write("data.xml")
                break

    def add_launch(self, board_name, launch_name, launch_desc, launch_file_path, launch_image_path):
        for data_element in self.root.findall("board"):
            if data_element.get("name") == str(board_name):
                launch_element = ElTree.SubElement(data_element, "launch")
                launch_element.set('id', board_name)
                # название
                launch_n = ElTree.SubElement(launch_element, "name")
                launch_n.text = launch_name
                # описание
                launch_d = ElTree.SubElement(launch_element, "description")
                launch_d.text = launch_desc
                # путь к файлу
                launch_fp = ElTree.SubElement(launch_element, "path")
                launch_fp.text = str(launch_file_path)
                # # путь к изображению
                launch_ip = ElTree.SubElement(launch_element, "image")
                launch_ip.text = launch_image_path
                tree = ElTree.ElementTree(self.root)
                tree.write("data.xml")
                break

    def get_launch_by_board_name(self, board_name):
        launch_list = []
        for board in self.root.findall('board'):
            if board.attrib.get('name') == board_name:
                for launch in board.findall('launch'):
                    launch_list.append(launch)
        return launch_list

    def remove_launch_item(self, board_name, launch_name):
        for board in self.root.findall('board'):
            if board.attrib.get('name') == board_name:
                for launch in board.findall('launch'):
                    if launch.find('name').text == launch_name:
                        board.remove(launch)
                        tree = ElTree.ElementTree(self.root)
                        tree.write("data.xml")
                        break
