import sys
import xml.etree.ElementTree as ET
import argparse

# Функция для чтения XML из файла
def read_xml(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Функция для парсинга XML
def parse_xml(xml_data):
    root = ET.fromstring(xml_data)
    parsed_data = {}
    
    for element in root.iter():
        if element.tag == 'application':
            parsed_data['name'] = element.find('name').text
            parsed_data['version'] = element.find('version').text
            parsed_data['settings'] = {}
            for setting in element.findall('.//setting'):
                key = setting.attrib.get('key')
                value = setting.text
                parsed_data['settings'][key] = value
            parsed_data['features'] = [feature.text for feature in element.findall('.//feature')]
    
    return parsed_data

# Функция для преобразования данных в конфигурационный язык
def convert_to_config(data):
    config_lines = []
    config_lines.append(f"% Конфигурация для {data['name']}")
    config_lines.append(f"const appName = '{data['name']}'")
    config_lines.append(f"const version = '{data['version']}'")
    
    settings = data['settings']
    settings_lines = []    
    for key, value in settings.items():
        settings_lines.append(f"    {key}: {value}")
    
    config_lines.append("settings = $[")
    config_lines.append(",\n".join(settings_lines))
    config_lines.append("]")
    
    features = data['features']
    config_lines.append("features = << " + ", ".join(features) + " >>")

    return "\n".join(config_lines)

# Функция для записи результата в файл
def write_output(config_data, output_file):
    with open(output_file, 'w') as f:
        f.write(config_data)

# Главная функция для обработки командной строки
def main():
    parser = argparse.ArgumentParser(description='XML to Configuration Language Converter')
    parser.add_argument('input', help='Input XML file path')
    parser.add_argument('--output', required=True, help='Output file path for the configuration')
    
    args = parser.parse_args()
    
    xml_data = read_xml(args.input)  # Читаем XML из указанного файла
    parsed_data = parse_xml(xml_data)  # Парсим XML
    config_data = convert_to_config(parsed_data)  # Преобразуем в конфигурационный язык
    write_output(config_data, args.output)  # Записываем результат в файл

if __name__ == "__main__":
    main()
