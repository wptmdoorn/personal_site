# imports
import io
import pandas as pd
import urllib.request
import json


def download_bv_data() -> io.BytesIO:
    url = "https://biologicalvariation.eu/api/meta_calculations"
    res = []

    with urllib.request.urlopen(url) as url:
        data = json.load(url)

    if data["code"] == "success":
        table = data["data"]

        for t in table:
            analyte = {
                "id": t["analyte"]["id"],
                "display_name": t["analyte"]["display_name"].strip(),
                "matrix": t["metas"][0]["matrix"]["matrix_expansion"] if "matrix" in t["metas"][0] else -1,
                "BV_within_median": -1,
                "BV_within_low": -1,
                "BV_within_high": -1,
                "BV_between_median": -1,
                "BV_between_low": -1,
                "BV_between_high": -1,
            }

            # cvi = within, cvg = between
            for meta in t["metas"]:
                if meta["var_type"] == ":cvi":
                    analyte["BV_within_median"] = meta["median"]
                    analyte["BV_within_low"] = float(meta["lower"])
                    analyte["BV_within_high"] = float(meta["upper"])
                elif meta["var_type"] == ":cvg":
                    analyte["BV_between_median"] = meta["median"]
                    analyte["BV_between_low"] = float(meta["lower"])
                    analyte["BV_between_high"] = float(meta["upper"])

            res.append(analyte)

    df = pd.DataFrame.from_dict(
        res
    )

    # aps calculations
    df["aps_bias"] = (
        0.25 * (df["BV_within_median"] ** 2 +
                df["BV_between_median"] ** 2) ** 0.5
    )
    df["aps_error"] = 1.65 * 0.5 * df["BV_within_median"] + df["aps_bias"]

    # export to excel
    b_buf = io.BytesIO()
    df.to_excel(b_buf, index=False)
    b_buf.seek(0)

    return b_buf
