import os
import matplotlib.pyplot as plt
from nhl_helpers import generic_csv_reader
from collections import defaultdict

ind_dict = generic_csv_reader(csv_file_path=os.path.join("Data_download", "ind_data.csv"), dict_key_attribute='Player', output_attributes=False)
bio_dict = generic_csv_reader(csv_file_path=os.path.join("Data_download", "bio_data.csv"), dict_key_attribute='Player', output_attributes=False)

draft_position = defaultdict(int)
players_drafted_per_position = defaultdict(int)
attribute = 'Goals'
for player_name in bio_dict:
    if int(bio_dict[player_name]['Age']) > 24:
        try:
            value = int(ind_dict[player_name][attribute])
        except:  # noqa
            value = int(onice_dict[player_name][attribute])
            except:  # noqa
                value = 0
                print('Could not find individual data for player ' + player_name)
        draft_position[bio_dict[player_name]['Overall Draft Position']] += value
        players_drafted_per_position[bio_dict[player_name]['Overall Draft Position']] += 1

max = 0
for pos in players_drafted_per_position:
    if players_drafted_per_position[pos] > max and pos != '-':
        max = players_drafted_per_position[pos]  # max is the number of drafts that players in the selection are available from.
        max_pos = pos

draft_position_sorted = []
for position in draft_position:
    gp = draft_position[position]
    if position == '-':
        position = 999
    else:
        position = int(position)
    draft_position_sorted.append((position, gp))

draft_position_sorted.sort()

step = 10
section_value = 0
last_section_value = 0
section_values, section_values_label = [], []
for i, entry in enumerate(draft_position_sorted):
    if (i % step == 0) and (i > 0):
        if i == step:
            diff = section_value
        else:
            diff = last_section_value - section_value

        print(f'Average games played for selection: [{i-step} - {i}]: {section_value}. Diff: {diff}')
        last_section_value = section_value
        section_values.append(section_value)
        section_values_label.append(i)
        section_value = 0

    section_value += (entry[1] / step / max)  # Average

plt.figure()
plt.plot(section_values_label, section_values)
plt.xlabel('Draft position')
plt.ylabel(attribute)
plt.show()