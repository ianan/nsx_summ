# nsx_summ
Summary plots of NuSTAR solar obs with other X-ray data.

To see overview info check out [index.md](index.md) or [https://ianan.github.io/nsx_summ/](https://ianan.github.io/nsx_summ/)

Some info/caveats:

* Bottom panel lightcurve for whole NuSTAR field of view, FPMA, FPMB and 2-10 keV
* 3rd panel lightcurve for NuSTAR per detector quadrant/id FPMA and 2-10 keV
* Map for Nustar just FPMA, over whole pointing and 2-10 keV, white numbers indicate detector quadrant/id
* Source of features in NuSTAR might not be in the field of view, i.e ghost rays from elsewhere on the solar disk
* NuSTAR pointing is not corrected, so could be up to ~ arcmin off
* GOES flare list being used is from SSW latest events so some/many of the smaller events likely to be missing
* STIX lightcurve is quicklook only in 4-10 keV, so smaller features might actually be there (need to create own lightcurves from spectrogram/pixel data over narrower energy range)

To do:

* ~~More NuSTAR campaigns~~
* ~~Add in XSM data~~
* ~~Nice web interface to the plots~~
