import math


def calculate_drywall_materials(area, perimeter):
  if perimeter <= 0 or area <= 0:
    return None

  height = area / perimeter
  profile_length = 2.60

  # 1. Tracks: Floor + Ceiling (perimeter * 2) / 2.60m profile length
  tracks = math.ceil(((perimeter * 2) / profile_length) * 0.35)

  # 2. Studs: Based on perimeter ratio (standard spacing calculation)
  base_studs_count = perimeter * 0.93

  if height > profile_length:
    studs = math.ceil(
        (base_studs_count * ((height + 0.30) / profile_length)) * 1.05
    )
    t1_screws_splice = math.ceil(base_studs_count) * 4
  else:
    studs = math.ceil(base_studs_count * 0.95)
    t1_screws_splice = 0

  # 3. Boards: Single face, 2.88m2 per board (1.20x2.40) + waste factor
  boards = math.ceil((area / 2.88) * 1.03)

  # 4. Anchors: Perimeter scaling (every ~0.37m)
  anchors = math.ceil(perimeter * 2.66)

  # 5. T1 Screws: Structure assembly + splices
  t1_screws = math.ceil(60 + t1_screws_splice)

  # 6. T2 Screws: Proportional to boards (~50 per board)
  t2_screws = math.ceil(boards * 50)

  # 7. Paper Tape: 1.32m per m2
  tape = round(area * 1.32, 2)

  # 8. Joint Compound: 0.60 kg per m2
  compound = round(area * 0.60, 2)

  return {
      "Tracks": tracks,
      "Studs": studs,
      "Boards": boards,
      "Anchors": anchors,
      "T1 Screws": t1_screws,
      "T2 Screws": t2_screws,
      "Paper Tape (m)": tape,
      "Joint Compound (kg)": compound,
      "Estimated Height": round(height, 2),
  }