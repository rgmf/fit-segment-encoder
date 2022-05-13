import fitparse


if __name__ == '__main__':
    fnames = [
        "segment_class.fit",
        "segment.fit",
        "fitfiles/segment_Albaterolo__últimos_4km_segment.fit",
        "fitfiles/2022-04-19-17-34-12.fit",
        "fitfiles/distance_time_nontype_error_1.fit",
        "fitfiles/distance_time_nontype_error_2.fit",
        "fitfiles/elevation_gain_nonetype_error_1.fit",
        "fitfiles/8484128986_ACTIVITY.fit",
        "fitfiles/8490929963_ACTIVITY.fit",
        "fitfiles/20220318_160201_Albaterolo.fit",
        "fitfiles/20170105_095829.fit",
        "fitfiles/20170106_091119.fit",
        "fitfiles/20170108_082319.fit"
    ]



    fitfile = fitparse.FitFile(fnames[0])

    # for m in fitfile.messages:
    #     print(m, m.get_values())

    for file_id in fitfile.get_messages("file_id"):
        print(file_id, type(file_id))
        fields = [field_data for field_data in file_id.fields]
        print(fields)
        if not list(filter(lambda field_data: field_data.field and field_data.field.def_num == 0 and field_data.value == "segment", fields)):
            print("It's not a segment file")
            exit()
        else:
            print("It's a segment file")

        print()
        print()
        for mesg in fitfile.messages:
            print(mesg.name, mesg.get_values())




    #     if list(filter(lambda field_data: field_data.field and field_data.field.def_num == 0, [field_data for field_data in file_id.fields])):
    #         print("Sí tiene 0:", )
    #     for field_data in file_id.fields:
    #         if field_data.field:
    #             print(
    #                 field_data.field.name,
    #                 f"({field_data.field.def_num})",
    #                 field_data.value,
    #                 f"({field_data.raw_value})"
    #             )
    #
    #
    # print()
    # print()
    #
    # sports = list(fitfile.get_messages("sport"))
    # sport = sports[0] if sports else None
    # if sport:
    #     field_data = list(filter(lambda fd: fd.field and fd.field.def_num == 0, sport.fields))
    #     if field_data:
    #         print("SIIII", field_data[0].value)
    #
    # for sport in fitfile.get_messages("sport"):
    #     print(sport)
    #     for field_data in sport.fields:
    #         if field_data.field:
    #             print(
    #                 "Field Name:", field_data.field.name,
    #                 "\nField Def Num:", field_data.field.def_num,
    #                 "\nField Value:", field_data.value,
    #                 "\nField Raw Value:", field_data.raw_value
    #             )
    #             print()
    #
    #

    # for record in fitfile.get_messages("segment"):
    #     print(record)
        # if "position_lat" in record.get_values() and "position_long" in record.get_values() and "timestamp" in record.get_values():
        #     lat = record.get_values()['position_lat'] / DIVIDE_LAT_LON
        #     lon = record.get_values()['position_long'] / DIVIDE_LAT_LON
        #     gpx.write(f"<trkpt lat=\"{lat}\" lon=\"{lon}\">\n")
        #     for data in record:
        #         if data.name == "timestamp":
        #             time = datetime.datetime.fromtimestamp(
        #                 data.value.timestamp(),
        #                 tz=datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        #             ).isoformat(timespec="milliseconds")
        #             gpx.write(f"<time>{time}</time>\n")
        #         elif data.name == "speed":
        #             gpx.write(f"<gpxtpx:speed>{data.value}</gpxtpx:speed>\n")
        #         elif data.name == "altitude":
        #             gpx.write(f"<ele>{data.value}</ele>\n")
        #         elif data.name == "cadence":
        #             gpx.write(f"<gpxtpx:cad>{data.value}</gpxtpx:cad>\n")
        #         elif data.name == "heart_rate":
        #             gpx.write(f"<gpxtpx:hr>{data.value}</gpxtpx:hr>\n")

    # for mesg in [m for m in fitfile.messages if m.name == "segment"]:
    #     print(mesg.get_values())

    # for mesg in [m for m in fitfile.messages if m.name == "event"]:
    #     print()
    #     for field_data in mesg.fields:
    #         print(
    #             type(field_data),
    #             type(field_data.field),
    #             field_data.field.name,
    #             field_data.field.def_num,
    #             field_data.field.scale,
    #             field_data.field.offset,
    #             field_data.raw_value,
    #             f"<aquí>{field_data.value} ({field_data.field.def_num})</aquí>"
    #         )



    #for mesg in [ m for m in fitfile.messages if m.name in ("record", "event")]:
    #    print(mesg)


    # for session in fitfile.get_messages("event"):
    #     print(type(session))
    #     print(session.def_mesg)
    #     print(session.fields)
    #     print("Name:", session.name)
    #     print("Mesg num:", session.mesg_num)
    #     print("Mesg type:", session.mesg_type)
    #     print("\tName:", session.mesg_type.name)
    #     print("\tNumber:", session.mesg_type.mesg_num)
    #     print("\tFields:", session.mesg_type.fields)
    #     print()