#!/usr/local/bin/ python3.5

import csv
import random
import pprint

# read in csv
# each record is a dict: {'name': 'ashley miller', 'level': 'senior', 'type':'infra', 'focus': 'be'}
# each group contains: seniors, (1) of each type
# make a senior set: senior, director, principal
# make a junior/mid set: junior, mid

DEV_TYPES = ['oo', 'infra', 'django']
DEN_SIZE = 5


def make_record(line):
    return {'name': line['name'], 'level': line['level'].lower(),
            'type': line['type'].lower(), 'focus': line['specialty'].lower()}


def make_junior_list(records):
    return [r for r in records if r['level'].lower() in ['junior', 'mid']]


def make_senior_list(records):
    return [r for r in records if r['level'].lower() not in ['junior', 'mid']]


def has_type(den, dev):
    dev_type = dev['type']
    dupes = [x for x in den if x['type'] == dev_type]
    return len(dupes) > 0


def init_dens(devs):
    # returns an array with the appropriate # of dens
    num_dens = int(len(devs) / DEN_SIZE)
    return [[] for i in range(num_dens)]


def make_dens(devs):
    # loop through dev types to add developers to dens
    dens = init_dens(devs)
    unassigned_devs = []
    assigned_count = 0
    for dev in devs:
        assigned = False
        for i in range(len(dens)):
            den = dens[i]
            # den is full, don't add
            if len(den) == DEN_SIZE:
                continue

            if has_type(den, dev):
                continue

            den.append(dev)
            print("{} has been assigned to den #{} which has {} people in it".format(dev['name'], i, len(den)))
            assigned = True
            assigned_count += 1
            break

        if not assigned:
            # have tried all the dens. they are full or duplicated
            unassigned_devs.append(dev)

    while len(unassigned_devs) > 0:
        for den in dens:
            # den is full, but there are others that are not
            if len(den) == DEN_SIZE and not all_full(dens):
                continue

            den.append(unassigned_devs.pop())
            break

    return dens


def all_full(dens):
    return all([len(dens) == DEN_SIZE for den in dens])


def print_dens(dens):
    for den in dens:
        pprint.pprint(den)


def make_dev_dens(filepath):
    records = []
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            records.append(make_record(line))
    #shuffle here because the original csv is roughly grouped by teams
    random.shuffle(records)

    juniors = make_junior_list(records)
    junior_dens = make_dens(juniors)
    seniors = make_senior_list(records)
    senior_dens = make_dens(seniors)
    all_dens = junior_dens + senior_dens
    make_csv(all_dens)
    print("Assigned {} to {} dens".format(len(records), len(all_dens)))


def make_csv(dens):
    with open('developer_dens.csv', 'w') as csvfile:
        fieldnames = dens[0][0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for den in dens:
            for developer in den:
                writer.writerow(developer)
            writer.writerow({'name': '', 'level': '', 'type': '', 'focus': '', 'type': ''})


if __name__ == '__main__':
    make_dev_dens("/tmp/devs.csv")
