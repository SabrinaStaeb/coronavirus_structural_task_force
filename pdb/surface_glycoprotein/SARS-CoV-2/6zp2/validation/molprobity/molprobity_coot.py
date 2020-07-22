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
data['rama'] = []
data['omega'] = []
data['rota'] = [('A', ' 516 ', 'GLU', 0.14623865503283884, (136.141, 113.13000000000002, 163.721)), ('A', '1113 ', 'THR', 0.028693333370793418, (130.918, 129.337, 61.07999999999999)), ('B', ' 516 ', 'GLU', 0.14773392678791883, (155.29, 147.433, 163.73199999999997)), ('B', '1113 ', 'THR', 0.028718210659852497, (143.867, 134.80600000000004, 61.091)), ('C', ' 516 ', 'GLU', 0.14697782430022166, (116.002, 146.858, 163.712)), ('C', '1113 ', 'THR', 0.02868297519081454, (132.646, 143.266, 61.072))]
data['cbeta'] = [('A', ' 900 ', 'TYR', ' ', 0.3329931149944986, (129.799, 146.72, 82.355)), ('B', ' 900 ', 'TYR', ' ', 0.333028276323168, (129.373, 125.14500000000002, 82.366)), ('C', ' 900 ', 'TYR', ' ', 0.33091848417020026, (148.261, 135.54900000000006, 82.346))]
data['probe'] = [(' A 334  ASN  ND2', ' A 360  ASN  O  ', -0.778, (126.42, 101.548, 174.025)), (' B 334  ASN  ND2', ' B 360  ASN  O  ', -0.777, (170.168, 144.781, 174.051)), (' C 334  ASN  ND2', ' C 360  ASN  O  ', -0.765, (111.237, 160.593, 173.799)), (' B1086  PRO  O  ', ' C 909  GLN  NE2', -0.66, (147.435, 137.237, 72.201)), (' A 807  LYS  NZ ', ' A 809  SER  OG ', -0.647, (117.861, 164.961, 107.064)), (' C 807  LYS  NZ ', ' C 809  SER  OG ', -0.644, (169.979, 136.859, 107.088)), (' B 807  LYS  NZ ', ' B 809  SER  OG ', -0.643, (119.852, 105.774, 107.19)), (' A1086  PRO  O  ', ' B 909  GLN  NE2', -0.637, (130.866, 125.555, 72.181)), (' A 909  GLN  NE2', ' C1086  PRO  O  ', -0.636, (128.691, 144.849, 72.419)), (' A 831  LYS  N  ', ' C 614  ASP  OD1', -0.627, (124.098, 164.777, 127.932)), (' A 614  ASP  OD1', ' B 831  LYS  N  ', -0.621, (116.378, 111.109, 127.906)), (' B 454  ARG  NH2', ' B 467  ASP  O  ', -0.616, (142.916, 163.985, 180.454)), (' C 454  ARG  NH2', ' C 467  ASP  O  ', -0.607, (107.722, 127.904, 180.607)), (' A 454  ARG  NH2', ' A 467  ASP  O  ', -0.599, (156.678, 115.543, 180.467)), (' C 100  ILE HD11', ' C 263  ALA  HB3', -0.597, (166.25, 184.542, 159.029)), (' B 100  ILE HD11', ' B 263  ALA  HB3', -0.589, (163.002, 85.161, 159.039)), (' A 100  ILE HD11', ' A 263  ALA  HB3', -0.581, (78.315, 137.42, 159.499)), (' A 395  VAL HG12', ' A 515  PHE  HB3', -0.578, (133.654, 112.331, 169.425)), (' B 395  VAL HG12', ' B 515  PHE  HB3', -0.576, (156.955, 145.42, 168.984)), (' B 614  ASP  OD1', ' C 831  LYS  N  ', -0.572, (166.939, 131.182, 127.8)), (' B 732  VAL HG22', ' B 854  LEU HD23', -0.568, (125.202, 122.904, 132.38)), (' C 395  VAL HG12', ' C 515  PHE  HB3', -0.564, (116.667, 149.59, 169.288)), (' A1090  VAL HG13', ' A1103  ARG  HE ', -0.563, (124.716, 126.012, 76.646)), (' C1090  VAL HG13', ' C1103  ARG  HE ', -0.561, (133.194, 150.166, 76.574)), (' A 732  VAL HG22', ' A 854  LEU HD23', -0.557, (129.935, 151.343, 132.43)), (' C 732  VAL HG22', ' C 854  LEU HD23', -0.557, (152.013, 132.816, 132.006)), (' C 326  ILE HD11', ' C 533  LEU HD12', -0.551, (119.361, 169.332, 155.648)), (' C 712  THR  N  ', ' C1067  GLN  O  ', -0.549, (144.517, 157.161, 79.733)), (' A 326  ILE HD11', ' A 533  LEU HD12', -0.549, (115.032, 104.849, 155.669)), (' B 326  ILE HD11', ' B 533  LEU HD12', -0.549, (172.77, 133.816, 155.437)), (' B1090  VAL HG13', ' B1103  ARG  HE ', -0.547, (149.817, 130.915, 76.665)), (' B 501  ASN  OD1', ' B 502  GLY  N  ', -0.545, (134.641, 144.121, 194.549)), (' B 933  SER  O  ', ' B 937  THR HG22', -0.541, (140.252, 106.767, 105.69)), (' A 933  SER  O  ', ' A 937  THR HG22', -0.539, (108.074, 146.903, 105.405)), (' C 501  ASN  OD1', ' C 502  GLY  N  ', -0.537, (129.361, 130.392, 194.369)), (' B 358  ILE  HB ', ' B 395  VAL HG23', -0.535, (160.235, 147.3, 173.281)), (' C 933  SER  O  ', ' C 937  THR HG22', -0.534, (158.722, 154.138, 105.663)), (' A 807  LYS  NZ ', ' A 809  SER  O  ', -0.524, (117.787, 164.418, 106.157)), (' C 358  ILE  HB ', ' C 395  VAL HG23', -0.523, (113.691, 151.289, 173.261)), (' A 115  GLN  HB2', ' A 233  ILE HD12', -0.52, (101.418, 132.98, 175.088)), (' A 358  ILE  HB ', ' A 395  VAL HG23', -0.519, (133.507, 108.993, 173.27)), (' A 501  ASN  OD1', ' A 502  GLY  N  ', -0.517, (143.743, 132.957, 194.37)), (' A 712  THR  N  ', ' A1067  GLN  O  ', -0.516, (112.704, 132.812, 79.651)), (' C 863  ASP  OD1', ' C 864  GLU  N  ', -0.513, (164.299, 132.744, 110.95)), (' A 863  ASP  OD1', ' A 864  GLU  N  ', -0.513, (124.175, 161.944, 110.908)), (' B 863  ASP  OD1', ' B 864  GLU  N  ', -0.512, (118.722, 112.771, 110.542)), (' C 115  GLN  HB2', ' C 233  ILE HD12', -0.508, (150.49, 166.837, 175.181)), (' B  63  THR  HG1', ' B  65  PHE  HE1', -0.506, (166.361, 97.779, 156.946)), (' B 712  THR  N  ', ' B1067  GLN  O  ', -0.506, (149.839, 117.497, 79.813)), (' B 115  GLN  HB2', ' B 233  ILE HD12', -0.505, (155.509, 107.677, 175.076)), (' C 870  THR  O  ', ' C 874  LEU HD23', -0.505, (158.889, 134.328, 98.245)), (' B 870  THR  O  ', ' B 874  LEU HD23', -0.495, (123.113, 116.663, 98.429)), (' A 870  THR  O  ', ' A 874  LEU HD23', -0.494, (125.569, 156.409, 98.403)), (' C 437  ASN  OD1', ' C 438  SER  N  ', -0.485, (126.51, 139.984, 189.981)), (' B 437  ASN  OD1', ' B 438  SER  N  ', -0.483, (144.03, 141.933, 190.025)), (' C 127  VAL HG21', ' C1603  NAG  H82', -0.483, (165.778, 173.105, 175.228)), (' A 437  ASN  OD1', ' A 438  SER  N  ', -0.482, (136.668, 125.676, 190.098)), (' A1007  GLN  OE1', ' A1010  ARG  NH1', -0.482, (127.887, 144.184, 125.293)), (' B1007  GLN  OE1', ' B1010  ARG  NH1', -0.48, (132.937, 124.826, 125.138)), (' C1007  GLN  OE1', ' C1010  ARG  NH1', -0.479, (146.453, 138.557, 124.932)), (' B 127  VAL HG21', ' B1302  NAG  H82', -0.478, (153.024, 91.255, 175.403)), (' A 127  VAL HG21', ' A1302  NAG  H82', -0.469, (88.717, 143.072, 175.372)), (' B 490  PHE  CE2', ' B 492  LEU  HB2', -0.467, (140.217, 165.217, 188.648)), (' A 490  PHE  CE2', ' A 492  LEU  HB2', -0.459, (159.416, 117.358, 189.013)), (' C 490  PHE  CE2', ' C 492  LEU  HB2', -0.454, (107.937, 124.685, 188.991)), (' B 807  LYS  NZ ', ' B 809  SER  O  ', -0.445, (119.949, 105.979, 106.392)), (' C 392  PHE  CD1', ' C 517  LEU HD21', -0.442, (120.002, 151.422, 165.571)), (' C 883  THR  HB ', ' C 890  LEU HD12', -0.441, (150.947, 124.796, 85.879)), (' C 357  ARG  NH2', ' C 396  TYR  OH ', -0.441, (107.659, 147.488, 169.463)), (' B 883  THR  HB ', ' B 890  LEU HD12', -0.44, (118.507, 128.005, 85.457)), (' A 392  PHE  CD1', ' A 517  LEU HD21', -0.44, (130.277, 114.117, 165.967)), (' B 392  PHE  CD1', ' B 517  LEU HD21', -0.439, (157.404, 142.002, 165.897)), (' C 901  ARG  NH1', ' C1045  LEU  O  ', -0.439, (148.92, 138.151, 89.232)), (' B1125  VAL HG13', ' B1128  ILE  HB ', -0.438, (158.135, 140.455, 68.719)), (' C 965  ASN  OD1', ' C 971  SER  N  ', -0.438, (148.969, 142.486, 149.948)), (' A 965  ASN  OD1', ' A 971  SER  N  ', -0.437, (123.208, 143.962, 149.853)), (' C 326  ILE HG23', ' C 541  PHE  HA ', -0.437, (123.779, 165.59, 155.437)), (' A 357  ARG  NH2', ' A 396  TYR  OH ', -0.435, (139.818, 105.523, 169.571)), (' B 965  ASN  OD1', ' B 971  SER  N  ', -0.434, (135.072, 120.841, 149.937)), (' A 326  ILE HG23', ' A 541  PHE  HA ', -0.434, (115.918, 110.095, 155.467)), (' B 357  ARG  NH2', ' B 396  TYR  OH ', -0.433, (160.48, 154.352, 169.543)), (' B 203  ILE  HB ', ' B 227  VAL HG12', -0.432, (147.512, 99.291, 163.299)), (' C 203  ILE  HB ', ' C 227  VAL HG12', -0.432, (161.908, 163.993, 163.472)), (' C1125  VAL HG13', ' C1128  ILE  HB ', -0.432, (120.539, 152.77, 68.551)), (' A 901  ARG  NH1', ' A1045  LEU  O  ', -0.431, (127.089, 146.099, 89.089)), (' C 563  GLN  O  ', ' C 577  ARG  NH2', -0.43, (107.346, 157.978, 155.383)), (' B 804  ASP  N  ', ' B 804  ASP  OD1', -0.43, (120.531, 105.695, 100.278)), (' B 326  ILE HG23', ' B 541  PHE  HA ', -0.429, (167.604, 131.425, 155.494)), (' C1090  VAL  CG1', ' C1103  ARG  HE ', -0.429, (132.878, 150.601, 76.827)), (' A1090  VAL  CG1', ' A1103  ARG  HE ', -0.428, (124.547, 125.868, 76.783)), (' A 295  PRO  HB3', ' A 597  VAL HG22', -0.427, (106.563, 126.329, 131.666)), (' C 295  PRO  HB3', ' C 597  VAL HG22', -0.426, (142.177, 165.947, 131.621)), (' B 295  PRO  HB3', ' B 597  VAL HG22', -0.426, (158.691, 115.29, 131.677)), (' A 203  ILE  HB ', ' A 227  VAL HG12', -0.425, (98.405, 143.982, 163.22)), (' A1125  VAL HG13', ' A1128  ILE  HB ', -0.423, (129.096, 114.059, 68.793)), (' A 883  THR  HB ', ' A 890  LEU HD12', -0.422, (137.736, 154.703, 85.462)), (' A 560  LEU  O  ', ' A 577  ARG  NH2', -0.42, (131.927, 98.658, 155.084)), (' A 395  VAL HG22', ' A 524  VAL HG21', -0.419, (132.082, 108.617, 171.201)), (' C 560  LEU  O  ', ' C 577  ARG  NH2', -0.418, (105.46, 157.278, 155.078)), (' B 395  VAL HG22', ' B 524  VAL HG21', -0.415, (161.589, 145.967, 171.323)), (' B 560  LEU  O  ', ' B 577  ARG  NH2', -0.414, (169.842, 150.987, 155.026)), (' C 569  ILE  H  ', ' C 569  ILE HD12', -0.411, (116.032, 152.285, 140.324)), (' B 569  ILE  H  ', ' B 569  ILE HD12', -0.41, (159.984, 144.664, 140.34)), (' B1090  VAL  CG1', ' B1103  ARG  HE ', -0.406, (150.09, 131.16, 76.819)), (' B 901  ARG  NH1', ' B1045  LEU  O  ', -0.405, (131.35, 123.43, 89.332)), (' C 898  MET  HE2', ' C1046  MET  SD ', -0.405, (153.652, 139.864, 87.857)), (' A 569  ILE  H  ', ' A 569  ILE HD12', -0.404, (131.527, 110.728, 140.623)), (' C 395  VAL HG22', ' C 524  VAL HG21', -0.403, (114.021, 153.036, 171.123)), (' B 196  ASN  ND2', ' B 233  ILE  O  ', -0.403, (154.081, 109.555, 168.469)), (' A 196  ASN  ND2', ' A 233  ILE  O  ', -0.402, (103.932, 132.888, 168.791)), (' B 898  MET  HE2', ' B1046  MET  SD ', -0.4, (129.873, 117.9, 87.408))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
