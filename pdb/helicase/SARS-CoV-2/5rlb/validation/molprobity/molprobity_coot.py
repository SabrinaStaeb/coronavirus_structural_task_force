# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = [('A', '   6 ', 'VAL', 0.08556307750383003, (3.4850000000000003, 41.13499999999999, -60.15699999999998)), ('A', '  48 ', 'TYR', 0.03991317205450157, (-0.7289999999999921, 58.402999999999984, -52.079)), ('A', ' 195 ', 'ILE', 0.08672121397687396, (-35.15299999999999, 28.510999999999996, -54.431999999999995)), ('A', ' 218 ', 'LYS', 0.04911710589549433, (-43.771, 25.010999999999996, -57.26499999999999)), ('A', ' 484 ', 'VAL', 0.01883497776557338, (-32.921, 37.66099999999997, -80.637)), ('B', '  10 ', 'SER', 0.041207603371876456, (9.544, 3.4759999999999964, -37.23799999999999)), ('B', '  48 ', 'TYR', 0.004730124975769358, (-2.5930000000000017, -9.476000000000003, -46.61899999999999)), ('B', '  92 ', 'LEU', 0.019212469030715277, (9.236000000000004, -3.297000000000004, -45.95499999999999)), ('B', ' 189 ', 'LYS', 0.03228965543678842, (-35.90599999999999, 12.547999999999995, -61.06599999999999)), ('B', ' 214 ', 'THR', 0.008225288735175983, (-31.51099999999999, 26.214, -41.203)), ('B', ' 283 ', 'PRO', 0.05947888258221115, (-15.560999999999995, 32.232, -15.580999999999998))]
data['omega'] = []
data['rota'] = [('A', '  12 ', 'THR', 0.0014849627099657813, (7.293, 46.752, -52.359)), ('A', '  26 ', 'CYS', 0.10608737375072519, (7.763000000000003, 47.595, -57.424)), ('A', '  35 ', 'ILE', 0.024148347417921306, (3.3440000000000083, 57.20399999999999, -66.502)), ('A', '  44 ', 'SER', 0.0478258166953647, (1.1069999999999993, 51.82, -49.808)), ('A', '  46 ', 'ASN', 0.06394101374475937, (-2.2479999999999922, 54.51899999999999, -46.884999999999984)), ('A', '  81 ', 'PHE', 0.014072196605345777, (10.617000000000003, 65.07099999999997, -53.033)), ('A', '  86 ', 'ASN', 0.2322145104739111, (14.137000000000006, 58.824, -61.926)), ('A', ' 173 ', 'ARG', 0.0, (-31.589999999999986, 40.56699999999999, -70.921)), ('A', ' 209 ', 'VAL', 0.022463310153487837, (-40.29299999999998, 30.194999999999986, -72.069)), ('A', ' 215 ', 'THR', 0.14424401021233374, (-34.63099999999999, 21.770999999999994, -57.012)), ('A', ' 220 ', 'ASN', 0.1449635918828181, (-44.346, 31.257999999999996, -57.339)), ('A', ' 255 ', 'THR', 0.04390138209725439, (3.4439999999999964, -3.237000000000002, -63.251999999999995)), ('A', ' 257 ', 'ASN', 0.20005698970969535, (2.0660000000000034, -7.493000000000013, -65.923)), ('A', ' 392 ', 'ARG', 0.0956526972611837, (0.6420000000000021, 18.836999999999993, -54.82599999999999)), ('A', ' 502 ', 'ARG', 0.0036088114640187166, (-36.86899999999999, 8.120999999999995, -96.862)), ('A', ' 530 ', 'THR', 0.01495926990173757, (-31.154999999999983, 17.597999999999992, -79.725)), ('A', ' 591 ', 'GLU', 0.04817842337656895, (-30.060999999999993, 16.849999999999987, -103.687)), ('B', '  46 ', 'ASN', 0.02784342349096451, (-2.0520000000000005, -4.825000000000001, -51.193)), ('B', '  95 ', 'ASN', 0.007557507266575577, (15.537000000000003, -3.8500000000000014, -40.278)), ('B', ' 103 ', 'VAL', 0.12875177361236348, (1.1560000000000006, -1.7410000000000023, -26.886)), ('B', ' 144 ', 'THR', 0.1363328681626579, (-20.093, 6.015999999999995, -38.544999999999995)), ('B', ' 164 ', 'HIS', 0.07431984844924497, (-45.681999999999995, 13.715999999999994, -39.032)), ('B', ' 192 ', 'LYS', 0.09698727145949734, (-31.828, 13.752, -54.318)), ('B', ' 220 ', 'ASN', 0.06080422309298907, (-43.59700000000001, 18.611999999999995, -48.996)), ('B', ' 247 ', 'VAL', 0.13666893646538752, (12.739999999999995, 36.19499999999999, -20.65)), ('B', ' 289 ', 'SER', 0.1906862864579314, (-14.103999999999996, 38.31399999999999, -25.611)), ('B', ' 353 ', 'GLU', 0.22723931886877027, (-6.230999999999998, 40.578999999999986, -43.39499999999999)), ('B', ' 361 ', 'ASN', 0.12137887947265334, (-12.707, 23.42, -39.57))]
data['cbeta'] = [('B', ' 253 ', 'TYR', ' ', 0.2778358390572814, (5.8710000000000075, 45.86499999999999, -31.217)), ('B', ' 534 ', 'ASP', ' ', 0.26146981961270505, (-26.315999999999992, 21.906999999999993, -23.425))]
data['probe'] = [(' B  12  THR HG21', ' B  25  LEU  O  ', -0.995, (3.588, -1.388, -39.977)), (' B  47  PRO  O  ', ' B 801  HOH  O  ', -0.787, (-3.918, -8.55, -50.404)), (' B  12  THR HG22', ' B  14  LEU  H  ', -0.718, (4.087, -1.029, -42.635)), (' B  86  ASN  HB3', ' B1023  HOH  O  ', -0.707, (13.21, -13.357, -35.084)), (' B 510  VAL HG21', ' B 541  TYR  CD1', -0.7, (-32.942, 34.63, -21.841)), (' B  48  TYR  OH ', ' B  90  PHE  O  ', -0.685, (4.272, -7.744, -45.446)), (' B 279  THR  HB ', ' B 429  MET  HE2', -0.682, (-5.849, 27.798, -20.528)), (' B  13  SER  O  ', ' B  44  SER  HA ', -0.671, (1.676, -1.898, -46.519)), (' A  13  SER  O  ', ' A  44  SER  HA ', -0.657, (2.095, 50.485, -50.982)), (' A 235  LEU HD21', ' A 382  TYR  CE2', -0.643, (-7.84, 32.427, -60.778)), (' B 163  LEU HD21', ' B 219  LEU HD11', -0.643, (-42.802, 18.893, -43.133)), (' A 293  ILE HG13', ' A 320  LYS  HB3', -0.623, (-11.43, 5.239, -67.61)), (' B 474 BMET  HG2', ' B 590  LEU  HB2', -0.615, (-38.43, 28.02, -3.009)), (' B 333  ILE  HB ', ' B 358  CYS  SG ', -0.611, (-11.764, 30.916, -41.701)), (' B 554  HIS  ND1', ' B 809  HOH  O  ', -0.61, (-25.884, 15.281, -19.963)), (' B   2  VAL  N  ', ' B 813  HOH  O  ', -0.602, (2.079, 2.538, -48.135)), (' A 510  VAL HG21', ' A 541  TYR  CD1', -0.593, (-27.104, 11.437, -80.011)), (' B 386  VAL  O  ', ' B 390  ARG  HG2', -0.592, (-5.415, 22.648, -38.99)), (' B 279  THR  HB ', ' B 429  MET  CE ', -0.588, (-6.307, 27.221, -20.664)), (' A 287  GLY  HA2', ' A 862  HOH  O  ', -0.587, (-10.708, 6.052, -75.541)), (' B 124  ASN HD21', ' B 381  ASN HD21', -0.579, (-7.473, 15.417, -24.45)), (' A 445  PRO  HB3', ' A 468  SER  HB3', -0.579, (-19.054, 5.475, -91.525)), (' B 277  TYR  HA ', ' B 396  TYR  O  ', -0.579, (-0.467, 30.184, -26.753)), (' B 174  PRO  O  ', ' B 803  HOH  O  ', -0.579, (-35.183, 9.704, -31.934)), (' A 130  LEU HD12', ' A 842  HOH  O  ', -0.572, (4.412, 39.782, -69.407)), (' A  59  ASP  OD1', ' A  61  THR  OG1', -0.571, (0.073, 62.28, -61.932)), (' B 504  PRO  HB3', ' B 507  ARG HH21', -0.556, (-47.835, 37.606, -12.971)), (' B   8  CYS  SG ', ' B  99  GLY  N  ', -0.553, (8.799, 0.053, -32.111)), (' B 367  THR  HA ', ' B 392  ARG  O  ', -0.547, (1.901, 31.008, -38.626)), (' B 124  ASN  ND2', ' B 381  ASN HD21', -0.543, (-6.92, 14.959, -24.38)), (' A 296  ALA  O  ', ' A 300  PRO  HA ', -0.543, (-2.49, 1.129, -61.333)), (' B 385  SER  OG ', ' B 802  HOH  O  ', -0.541, (-3.49, 17.073, -36.191)), (' A 255  THR HG23', ' A 300  PRO  HG3', -0.537, (0.918, -2.734, -61.483)), (' A 368  ALA  O  ', ' A 393  ALA  HA ', -0.536, (1.118, 14.084, -56.644)), (' B 442  ARG HH11', ' B 464  HIS  CE1', -0.53, (-17.77, 46.386, -12.117)), (' B  46  ASN  N  ', ' B  46  ASN  OD1', -0.528, (-0.85, -3.959, -52.212)), (' A 367  THR  HA ', ' A 392  ARG  O  ', -0.523, (-0.799, 16.288, -54.018)), (' B  12  THR  CG2', ' B  26  CYS  HA ', -0.523, (5.74, -1.005, -39.789)), (' B 278  SER  HA ', ' B 435  ASP  OD1', -0.518, (-0.733, 29.539, -21.265)), (' B  15  ARG  HG3', ' B  24  PHE  CD2', -0.517, (0.091, 2.458, -43.22)), (' A 512  ILE  HA ', ' A 531  GLN  O  ', -0.511, (-27.469, 19.851, -81.772)), (' B 401  ASP  OD1', ' B 403  ALA  HB3', -0.509, (-15.159, 26.762, -15.486)), (' A  14  LEU  HB2', ' A  25  LEU  O  ', -0.508, (4.996, 49.174, -56.131)), (' A  64  TYR  O  ', ' A  70  TYR  HA ', -0.508, (3.257, 63.791, -50.345)), (' B 252  LEU  HB3', ' B 299  TYR  CD1', -0.507, (2.473, 42.046, -28.955)), (' A  12  THR HG21', ' A  26  CYS  HA ', -0.503, (7.965, 48.232, -56.004)), (' A 277  TYR  HA ', ' A 396  TYR  O  ', -0.5, (2.649, 16.548, -66.288)), (' A 512  ILE  O  ', ' A 546  PHE  HA ', -0.499, (-26.726, 19.4, -87.072)), (' A  44  SER  OG ', ' A  45  VAL  N  ', -0.497, (1.84, 52.164, -47.847)), (' B 143  GLU  OE2', ' B 229  SER  HA ', -0.495, (-20.832, 13.076, -40.257)), (' B  14  LEU  HB2', ' B  25  LEU  O  ', -0.495, (2.932, -1.53, -39.99)), (' B  13  SER  HB2', ' B  92  LEU  HB2', -0.49, (7.377, -1.358, -46.635)), (' A  60  VAL  HB ', ' A 899  HOH  O  ', -0.488, (-0.377, 57.849, -56.805)), (' A 490  ARG  HB2', ' A 491  PRO  HD3', -0.484, (-37.474, 27.807, -92.435)), (' B 222  GLY  C  ', ' B 847  HOH  O  ', -0.482, (-40.137, 13.314, -50.297)), (' B  19  CYS  SG ', ' B 110  ALA  HB1', -0.473, (-7.311, -0.379, -33.588)), (' B 167  TRP  CZ3', ' B 174  PRO  HD2', -0.473, (-34.421, 9.133, -36.59)), (' B 533  VAL HG11', ' B 560  ARG  O  ', -0.472, (-25.49, 24.222, -16.614)), (' A 278  SER  HB2', ' A 436  MET  HE2', -0.468, (2.478, 13.794, -71.381)), (' B 120  TYR  CE2', ' B 409  ARG  HG2', -0.466, (-16.131, 11.28, -25.812)), (' B  28  LYS  O  ', ' B  32  ASP  OD1', -0.462, (5.345, -6.229, -31.709)), (' B 293  ILE HG13', ' B 320  LYS  HB3', -0.461, (-13.989, 41.654, -29.813)), (' B 373  PHE  CD1', ' B 387  VAL HG21', -0.461, (-8.114, 25.601, -31.889)), (' B 477  LYS  NZ ', ' B 551  GLU  OE2', -0.46, (-34.241, 13.896, -4.658)), (' B  34  VAL  O  ', ' B  40  LYS  NZ ', -0.459, (-4.857, -11.31, -32.797)), (' A  49  VAL HG23', ' A  58  THR HG22', -0.457, (-6.176, 61.708, -53.19)), (' A 257  ASN  C  ', ' A 257  ASN  ND2', -0.457, (0.331, -7.192, -66.498)), (' A 167  TRP  CZ3', ' A 174  PRO  HD2', -0.456, (-32.422, 38.42, -68.906)), (' B 377  SER  O  ', ' B 406  PRO  HA ', -0.455, (-16.197, 21.238, -23.479)), (' B   7  LEU HD13', ' B 103  VAL HG22', -0.454, (2.244, -0.908, -29.989)), (' A  19  CYS  HB2', ' A  23  PRO  HD2', -0.454, (-4.068, 46.985, -59.91)), (' B 368  ALA  O  ', ' B 393  ALA  HA ', -0.453, (1.774, 33.075, -35.771)), (' A  20  ILE HG22', ' A 876  HOH  O  ', -0.451, (-8.112, 45.529, -63.366)), (' A  12  THR  CG2', ' A  26  CYS  HA ', -0.451, (8.057, 47.781, -55.709)), (' B 213  GLY  C  ', ' B 215  THR  H  ', -0.447, (-33.723, 26.105, -41.5)), (' A  34  VAL  HA ', ' A  39  HIS  O  ', -0.446, (-0.411, 55.149, -63.773)), (' A  63  LEU  HB3', ' A  83  LEU HD12', -0.446, (2.489, 61.921, -54.303)), (' A 580  ASP  OD1', ' A 584  LYS  HE2', -0.445, (-12.807, 24.903, -97.359)), (' A 283  PRO  HG3', ' A 457  TYR  CE1', -0.441, (-6.732, 15.34, -83.12)), (' A 200  PHE  HA ', ' A 210  VAL  O  ', -0.439, (-35.857, 28.083, -69.41)), (' A  21  ARG  NH1', ' A 814  HOH  O  ', -0.438, (-11.53, 41.591, -57.795)), (' B 373  PHE  CE1', ' B 387  VAL HG21', -0.437, (-8.158, 25.212, -32.426)), (' B 488  ILE HD11', ' B 517  SER  HB3', -0.437, (-40.742, 15.816, -22.277)), (' B 183  THR  HG1', ' B 228  THR  CB ', -0.435, (-26.044, 16.49, -43.12)), (' B  13  SER  HG ', ' B  44  SER  HG ', -0.434, (3.552, -2.772, -46.679)), (' A  12  THR  HB ', ' A  14  LEU  H  ', -0.433, (5.445, 48.339, -53.4)), (' A  86  ASN  N  ', ' A  86  ASN HD22', -0.432, (14.312, 60.776, -61.52)), (' A 492  GLN  HG2', ' A 575  ILE HG21', -0.432, (-30.184, 22.493, -94.467)), (' B 551  GLU  HG2', ' B 577  SER  HB3', -0.431, (-33.525, 15.235, -7.933)), (' B 136  GLU  CD ', ' B 234  PRO  HA ', -0.43, (-6.392, 10.827, -38.655)), (' B 511  PHE  HB3', ' B 530  THR HG22', -0.43, (-38.521, 27.614, -20.583)), (' A  34  VAL HG12', ' A  39  HIS  O  ', -0.429, (-0.729, 55.083, -62.116)), (' B  95  ASN  N  ', ' B  95  ASN  OD1', -0.429, (14.661, -3.448, -41.706)), (' A  16  CYS  O  ', ' A  22  ARG  HA ', -0.429, (-4.445, 47.67, -57.322)), (' A 480  ILE HG21', ' A 550  THR HG22', -0.429, (-28.876, 32.526, -89.813)), (' B 139  LYS  HG2', ' B 232  VAL HG22', -0.428, (-14.118, 12.802, -37.726)), (' A 376  ILE HG12', ' A 425  VAL HG11', -0.428, (-4.063, 20.852, -71.026)), (' A 304  ILE  HA ', ' A 370  ILE  O  ', -0.427, (-3.479, 10.821, -59.522)), (' B 103  VAL  CG1', ' B 103  VAL  O  ', -0.426, (-0.363, -2.215, -28.015)), (' A   7  LEU HD22', ' A 103  VAL HG22', -0.425, (6.537, 45.113, -66.198)), (' A 462  LYS  HA ', ' A 462  LYS  HD3', -0.425, (-5.13, 8.408, -90.858)), (' A 519  ASN  HB3', ' A 530  THR  CG2', -0.425, (-31.768, 20.82, -79.502)), (' B 490  ARG  N  ', ' B 491  PRO  CD ', -0.424, (-44.055, 17.539, -13.316)), (' A 260  ASP  HA ', ' A 263  SER  OG ', -0.424, (-1.048, -5.252, -73.956)), (' A 487  ALA  HB1', ' A 550  THR  CG2', -0.423, (-28.407, 31.189, -88.083)), (' A 157  VAL HG21', ' A 219  LEU  O  ', -0.422, (-45.148, 29.661, -60.107)), (' A 318  CYS  HB3', ' A 343  PHE  CE2', -0.421, (-17.953, 7.224, -61.901)), (' A 215  THR HG22', ' B 193  VAL HG21', -0.421, (-31.733, 21.091, -55.43)), (' B 512  ILE  O  ', ' B 546  PHE  HA ', -0.418, (-34.485, 26.11, -15.069)), (' B 451  THR HG23', ' B 584  LYS  O  ', -0.418, (-23.899, 27.33, -3.983)), (' B 474 AMET  SD ', ' B 495  VAL HG11', -0.417, (-41.318, 24.758, -5.381)), (' B 455  LEU  HG ', ' B 456  VAL HG13', -0.417, (-19.05, 23.753, -9.104)), (' A 142  GLU  HA ', ' A 411  LEU HD11', -0.417, (-16.169, 39.635, -67.919)), (' A 266  VAL  O  ', ' A 270  GLN  HG3', -0.417, (5.761, 3.292, -70.39)), (' B 127  THR HG23', ' B 913  HOH  O  ', -0.416, (1.287, 6.681, -24.532)), (' A 405  LEU  CD1', ' A 534  ASP  HA ', -0.416, (-19.183, 22.618, -78.353)), (' A 318  CYS  HB3', ' A 343  PHE  CD2', -0.416, (-18.391, 7.622, -61.558)), (' B 508  LYS  HD3', ' B 973  HOH  O  ', -0.415, (-36.793, 41.425, -17.953)), (' A  72  CYS  SG ', ' A  74  SER  HB2', -0.415, (-2.125, 71.705, -54.504)), (' B   8  CYS  SG ', ' B  99  GLY  O  ', -0.414, (8.469, 0.795, -31.085)), (' B 121  ILE HG23', ' B 421  TYR  CE1', -0.414, (-8.501, 10.414, -17.415)), (' B 420  GLU  HG2', ' B 835  HOH  O  ', -0.413, (-10.657, 16.568, -14.427)), (' A 456  VAL HG23', ' A 457  TYR  CE2', -0.412, (-8.715, 17.832, -86.104)), (' A 472  PHE  HA ', ' A 588  THR  O  ', -0.412, (-23.567, 12.722, -98.623)), (' A 130  LEU  HA ', ' A 130  LEU HD23', -0.412, (1.039, 39.475, -64.864)), (' A 304  ILE HG12', ' A 370  ILE  HB ', -0.411, (-1.829, 9.395, -60.876)), (' B   9  ASN  O  ', ' B  10  SER  C  ', -0.411, (8.487, 4.666, -38.314)), (' A 115  THR  HA ', ' A 411  LEU  O  ', -0.411, (-15.576, 41.066, -74.786)), (' B 518  GLN  HA ', ' B 518  GLN  OE1', -0.411, (-40.0, 19.271, -18.349)), (' B  12  THR HG21', ' B  25  LEU  C  ', -0.41, (4.194, -0.566, -38.953)), (' B  50  CYS  SG ', ' B  71  TYR  HA ', -0.41, (-3.903, -17.647, -49.969)), (' A  23  PRO  HB3', ' A 701  VVJ  C9 ', -0.41, (-1.577, 41.968, -59.298)), (' A 456  VAL HG23', ' A 457  TYR  CD2', -0.409, (-8.3, 17.362, -86.415)), (' A 393  ALA  HB3', ' A 396  TYR  CZ ', -0.409, (0.819, 18.086, -59.313)), (' A  63  LEU  CB ', ' A  83  LEU HD12', -0.408, (2.496, 61.858, -54.458)), (' B 490  ARG  HB2', ' B 491  PRO  HD3', -0.407, (-45.615, 16.814, -13.222)), (' A  30  CYS  O  ', ' A  34  VAL HG22', -0.407, (3.63, 54.309, -62.27)), (' B 174  PRO  HG2', ' B 182  PHE  HZ ', -0.407, (-33.045, 11.745, -35.411)), (' B 152  ALA  HB2', ' B 167  TRP  CH2', -0.406, (-36.337, 10.465, -38.432)), (' B 269  TYR  OH ', ' B 294  GLY  HA3', -0.406, (-7.753, 43.292, -24.536)), (' A  33  HIS  HA ', ' A 107  ASN  OD1', -0.405, (1.736, 50.651, -66.396)), (' A 331  SER  HA ', ' A 347  LYS  O  ', -0.405, (-16.274, 8.122, -53.899)), (' A   7  LEU HD11', ' A 106  PHE  CG ', -0.403, (2.585, 45.12, -64.898)), (' A 303  ARG  NH1', ' A 353  GLU  O  ', -0.403, (-7.489, 9.167, -52.865)), (' B 152  ALA  HB2', ' B 167  TRP  CZ3', -0.403, (-36.14, 9.9, -38.27)), (' A 540  GLU  HA ', ' A 567  ARG  O  ', -0.402, (-20.884, 10.598, -81.415)), (' B 129  ARG  NH1', ' B 840  HOH  O  ', -0.402, (-2.001, 9.621, -37.677)), (' A 352  LEU HD11', ' B 234  PRO  HD3', -0.402, (-7.513, 11.626, -43.932)), (' B 249  ILE HG23', ' B 273  GLY  HA3', -0.4, (4.93, 39.276, -25.678)), (' A 176  LEU HD22', ' A 200  PHE  HB2', -0.4, (-33.862, 32.158, -69.591)), (' A 252  LEU  HB3', ' A 299  TYR  CD2', -0.4, (4.182, 4.803, -61.928)), (' B 593  PRO  HG2', ' B 877  HOH  O  ', -0.4, (-45.205, 27.726, -5.064))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
