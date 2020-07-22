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
data['rama'] = [('A', ' 198 ', 'ASP', 0.017750161560308078, (154.25, 159.949, 164.769)), ('A', ' 199 ', 'GLY', 0.03763827350219431, (157.54, 160.312, 166.72)), ('A', ' 518 ', 'LEU', 0.0197229151782158, (114.725, 151.824, 159.172)), ('B', ' 198 ', 'ASP', 0.017669813005239066, (147.296, 107.772, 164.81)), ('B', ' 199 ', 'GLY', 0.03730891951473522, (145.953, 104.745, 166.759)), ('B', ' 518 ', 'LEU', 0.01920126619163852, (160.141, 146.025, 159.221)), ('C', ' 198 ', 'ASP', 0.01725713929612825, (105.663, 139.72, 164.79)), ('C', ' 199 ', 'GLY', 0.03742479948738623, (103.70199999999997, 142.388, 166.74000000000004)), ('C', ' 518 ', 'LEU', 0.019730802332739373, (132.467, 109.558, 159.193))]
data['omega'] = []
data['rota'] = [('A', ' 309 ', 'GLU', 0.010523088154975208, (151.379, 161.053, 123.215)), ('A', ' 400 ', 'PHE', 0.040925791801849076, (114.574, 140.198, 183.612)), ('A', ' 429 ', 'PHE', 0.0031644916929687117, (119.528, 140.288, 166.462)), ('A', ' 986 ', 'GLU', 0.0, (145.932, 130.828, 157.529)), ('B', ' 309 ', 'GLU', 0.010500022710567635, (149.794, 109.675, 123.26)), ('B', ' 400 ', 'PHE', 0.04080820424018932, (150.105, 152.01, 183.63400000000004)), ('B', ' 429 ', 'PHE', 0.003091598712952242, (147.736, 147.672, 166.48)), ('B', ' 986 ', 'GLU', 0.0, (126.314, 129.588, 157.506)), ('C', ' 309 ', 'GLU', 0.010641018458397539, (106.138, 136.676, 123.235)), ('C', ' 400 ', 'PHE', 0.04066129942393677, (142.613, 115.246, 183.632)), ('C', ' 429 ', 'PHE', 0.003137348646524752, (140.055, 119.488, 166.481)), ('C', ' 986 ', 'GLU', 0.0, (135.038, 147.082, 157.545))]
data['cbeta'] = [('A', ' 429 ', 'PHE', ' ', 0.2907992312505349, (119.33699999999997, 139.611, 167.864)), ('A', ' 617 ', 'CYS', ' ', 0.276817998816199, (130.51, 174.463, 131.611)), ('A', ' 986 ', 'GLU', ' ', 0.318425531949599, (145.322, 129.376, 157.48100000000002)), ('B', ' 429 ', 'PHE', ' ', 0.28950468226710435, (147.243, 148.178, 167.881)), ('B', ' 617 ', 'CYS', ' ', 0.2766009499463512, (171.853, 120.98800000000003, 131.703)), ('B', ' 986 ', 'GLU', ' ', 0.3178697029014744, (125.364, 130.846, 157.455)), ('C', ' 429 ', 'PHE', ' ', 0.28945226987000927, (140.736, 119.661, 167.882)), ('C', ' 617 ', 'CYS', ' ', 0.2766699284301144, (104.965, 111.898, 131.635)), ('C', ' 986 ', 'GLU', ' ', 0.3189014261768628, (136.60099999999994, 147.28, 157.497))]
data['probe'] = [(' A 986  GLU  N  ', ' A 986  GLU  OE1', -0.693, (146.424, 130.428, 158.974)), (' B 986  GLU  N  ', ' B 986  GLU  OE1', -0.682, (125.638, 129.25, 158.872)), (' C 986  GLU  N  ', ' C 986  GLU  OE1', -0.676, (134.959, 148.02, 158.91)), (' B 376  THR HG22', ' B 435  ALA  HB3', -0.646, (147.25, 141.218, 181.887)), (' C 376  THR HG22', ' C 435  ALA  HB3', -0.638, (134.187, 122.971, 181.386)), (' A 376  THR HG22', ' A 435  ALA  HB3', -0.634, (125.281, 143.19, 181.803)), (' A 457  ARG  NH1', ' A 459  SER  OG ', -0.622, (109.239, 124.053, 173.319)), (' C 457  ARG  NH1', ' C 459  SER  OG ', -0.621, (159.543, 119.223, 173.261)), (' C 342  PHE  HE1', ' C 434  ILE HG21', -0.618, (132.15, 115.501, 180.41)), (' B 457  ARG  NH1', ' B 459  SER  OG ', -0.617, (138.967, 165.009, 173.474)), (' B 342  PHE  HE1', ' B 434  ILE HG21', -0.6, (155.205, 142.668, 180.511)), (' A 342  PHE  HE1', ' A 434  ILE HG21', -0.598, (120.551, 149.182, 180.117)), (' A 998  GLN  NE2', ' C1001  GLN  OE1', -0.594, (137.621, 140.512, 140.259)), (' B  91  TYR  OH ', ' B 191  GLU  OE2', -0.588, (154.506, 91.477, 148.159)), (' C 734  CYS  SG ', ' C 735  THR  N  ', -0.583, (136.197, 152.497, 140.67)), (' A 734  CYS  SG ', ' A 735  THR  N  ', -0.582, (150.064, 127.101, 140.64)), (' A  91  TYR  OH ', ' A 191  GLU  OE2', -0.579, (164.647, 174.131, 148.079)), (' B 734  CYS  SG ', ' B 735  THR  N  ', -0.575, (121.182, 127.805, 140.492)), (' C  91  TYR  OH ', ' C 191  GLU  OE2', -0.571, (88.072, 141.57, 148.031)), (' B1001  GLN  OE1', ' C 998  GLN  NE2', -0.564, (130.689, 134.985, 140.373)), (' C 226  LEU HD12', ' C 227  VAL HG23', -0.56, (92.788, 151.563, 159.974)), (' C 375  SER  N  ', ' C 435  ALA  O  ', -0.559, (131.055, 122.128, 183.864)), (' B 226  LEU HD12', ' B 227  VAL HG23', -0.556, (143.381, 90.747, 159.934)), (' A 375  SER  N  ', ' A 435  ALA  O  ', -0.555, (126.275, 146.828, 183.844)), (' A 226  LEU HD12', ' A 227  VAL HG23', -0.552, (170.292, 165.199, 159.792)), (' C 732  VAL HG22', ' C 854  LEU HD23', -0.547, (128.651, 151.435, 134.245)), (' A 457  ARG  NE ', ' A 467  ASP  OD1', -0.546, (108.791, 125.862, 177.123)), (' A 732  VAL HG22', ' A 854  LEU HD23', -0.544, (152.68, 133.789, 134.012)), (' A 809  SER  OG ', ' A 864  GLU  OE2', -0.54, (167.936, 135.799, 110.577)), (' A 442  ASP  OD2', ' A 451  TYR  OH ', -0.539, (114.138, 141.305, 191.762)), (' B 375  SER  N  ', ' B 435  ALA  O  ', -0.533, (149.798, 138.559, 183.78)), (' A1001  GLN  OE1', ' B 998  GLN  NE2', -0.533, (138.824, 131.64, 140.218)), (' B 732  VAL HG22', ' B 854  LEU HD23', -0.533, (125.431, 122.257, 134.069)), (' B 809  SER  OG ', ' B 864  GLU  OE2', -0.532, (119.611, 108.026, 110.498)), (' C 981  ASP  N  ', ' C 984  GLU  OE2', -0.524, (130.611, 149.954, 164.354)), (' C 442  ASP  OD2', ' C 451  TYR  OH ', -0.522, (141.85, 114.244, 191.8)), (' C 457  ARG  NE ', ' C 467  ASP  OD1', -0.516, (157.964, 117.484, 177.194)), (' B 981  ASP  N  ', ' B 984  GLU  OE2', -0.515, (125.873, 124.574, 164.245)), (' A 981  ASP  N  ', ' A 984  GLU  OE2', -0.512, (150.515, 133.038, 164.271)), (' B1007  GLN  OE1', ' B1010  ARG  NH1', -0.512, (133.626, 124.568, 127.043)), (' B 442  ASP  OD2', ' B 451  TYR  OH ', -0.511, (151.169, 151.822, 191.887)), (' C1007  GLN  OE1', ' C1010  ARG  NH1', -0.511, (127.346, 143.142, 127.026)), (' C 746  SER  O  ', ' C 750  LEU HD12', -0.511, (140.375, 153.152, 147.901)), (' B 457  ARG  NE ', ' B 467  ASP  OD1', -0.509, (140.583, 164.286, 177.126)), (' C 809  SER  OG ', ' C 864  GLU  OE2', -0.507, (119.64, 163.833, 110.527)), (' B 746  SER  O  ', ' B 750  LEU HD12', -0.506, (118.442, 131.246, 147.831)), (' A 746  SER  O  ', ' A 750  LEU HD12', -0.505, (148.217, 123.559, 148.02)), (' A 403  ARG  NH1', ' A 505  TYR  O  ', -0.503, (122.857, 133.761, 193.26)), (' A1007  GLN  OE1', ' A1010  ARG  NH1', -0.502, (146.738, 139.198, 127.264)), (' C 403  ARG  NH1', ' C 505  TYR  O  ', -0.498, (144.028, 125.547, 193.316)), (' B 430  THR  OG1', ' B 515  PHE  O  ', -0.498, (153.028, 146.564, 165.058)), (' B 807  LYS  O  ', ' B 810  LYS  NZ ', -0.497, (117.328, 102.194, 105.531)), (' B 201  PHE  CD1', ' B 203  ILE HD11', -0.496, (147.997, 94.886, 162.943)), (' B 787  THR  OG1', ' B 791  LYS  NZ ', -0.495, (120.176, 108.85, 93.646)), (' A  87  ASN  N  ', ' A  87  ASN  OD1', -0.494, (153.484, 174.353, 159.69)), (' A 201  PHE  CD1', ' A 203  ILE HD11', -0.492, (165.062, 166.995, 162.936)), (' C 787  THR  OG1', ' C 791  LYS  NZ ', -0.492, (120.181, 162.79, 93.731)), (' B 979  ARG  NH1', ' C 381  GLY  O  ', -0.491, (132.386, 119.554, 162.722)), (' C  87  ASN  N  ', ' C  87  ASN  OD1', -0.49, (93.555, 131.577, 159.311)), (' A 982  PRO  O  ', ' A 986  GLU  OE1', -0.49, (147.165, 129.984, 160.615)), (' B 490  PHE  CE2', ' B 492  LEU  HB2', -0.49, (140.414, 166.058, 188.458)), (' A 787  THR  OG1', ' A 791  LYS  NZ ', -0.489, (167.094, 135.786, 93.768)), (' C 490  PHE  CE2', ' C 492  LEU  HB2', -0.489, (159.649, 116.714, 188.423)), (' A 490  PHE  CE2', ' A 492  LEU  HB2', -0.488, (107.497, 125.138, 188.232)), (' C 201  PHE  CD1', ' C 203  ILE HD11', -0.488, (94.387, 145.188, 163.15)), (' C 807  LYS  O  ', ' C 810  LYS  NZ ', -0.487, (115.865, 168.62, 105.615)), (' C 982  PRO  O  ', ' C 986  GLU  OE1', -0.487, (135.367, 148.573, 160.249)), (' C 226  LEU  CD1', ' C 227  VAL HG23', -0.485, (92.484, 151.35, 159.605)), (' A 430  THR  OG1', ' A 515  PHE  O  ', -0.485, (117.857, 145.473, 165.01)), (' A 226  LEU  CD1', ' A 227  VAL HG23', -0.484, (171.062, 165.339, 160.008)), (' B  87  ASN  N  ', ' B  87  ASN  OD1', -0.482, (160.196, 101.21, 159.81)), (' B 226  LEU  CD1', ' B 227  VAL HG23', -0.48, (143.77, 90.447, 159.639)), (' A 454  ARG  NH2', ' A 467  ASP  O  ', -0.478, (107.318, 128.025, 181.08)), (' B 982  PRO  O  ', ' B 986  GLU  OE1', -0.477, (124.855, 129.027, 160.678)), (' C 898  MET  SD ', ' C1046  MET  HE3', -0.477, (122.721, 147.839, 88.408)), (' A 898  MET  SD ', ' A1046  MET  HE3', -0.476, (152.71, 141.176, 88.41)), (' B 403  ARG  NH1', ' B 505  TYR  O  ', -0.475, (140.518, 148.135, 193.37)), (' B 898  MET  SD ', ' B1046  MET  HE3', -0.474, (131.807, 118.476, 88.868)), (' C 454  ARG  NH2', ' C 467  ASP  O  ', -0.474, (156.811, 114.942, 181.183)), (' B 454  ARG  NH2', ' B 467  ASP  O  ', -0.473, (143.325, 164.507, 181.162)), (' B 946  ASP  OD1', ' B 947  VAL  N  ', -0.472, (137.881, 119.207, 119.099)), (' C 946  ASP  OD1', ' C 947  VAL  N  ', -0.47, (120.466, 142.132, 119.221)), (' C 430  THR  OG1', ' C 515  PHE  O  ', -0.468, (136.175, 115.516, 165.11)), (' A 165  ASN  OD1', ' A1321  NAG  N2 ', -0.467, (161.278, 168.557, 185.041)), (' A 946  ASP  OD1', ' A 947  VAL  N  ', -0.467, (149.434, 145.814, 119.396)), (' C 165  ASN  OD1', ' C1321  NAG  N2 ', -0.467, (94.603, 141.303, 184.961)), (' C1125  VAL HG13', ' C1128  ILE  HB ', -0.467, (130.372, 113.52, 70.868)), (' A1125  VAL HG13', ' A1128  ILE  HB ', -0.466, (119.356, 151.088, 71.081)), (' B 165  ASN  OD1', ' B1321  NAG  N2 ', -0.463, (151.243, 97.349, 185.075)), (' B 403  ARG  HG2', ' B 495  TYR  CE2', -0.463, (140.837, 151.346, 188.578)), (' B1125  VAL HG13', ' B1128  ILE  HB ', -0.461, (157.506, 142.482, 70.982)), (' C 494  SER  OG ', ' C 495  TYR  N  ', -0.459, (150.959, 120.054, 192.811)), (' C 435  ALA  HB2', ' C 510  VAL HG12', -0.456, (137.0, 121.548, 182.406)), (' B 494  SER  OG ', ' B 495  TYR  N  ', -0.455, (142.001, 157.138, 192.989)), (' A 403  ARG  HG2', ' A 495  TYR  CE2', -0.453, (119.773, 132.711, 188.522)), (' A 435  ALA  HB2', ' A 510  VAL HG12', -0.452, (123.038, 142.203, 182.08)), (' A 494  SER  OG ', ' A 495  TYR  N  ', -0.448, (114.277, 130.612, 193.193)), (' B 280  ASN  ND2', ' B 284  THR  OG1', -0.448, (139.572, 93.16, 138.435)), (' B 138  ASP  N  ', ' B 138  ASP  OD2', -0.447, (167.792, 83.845, 171.243)), (' B 435  ALA  HB2', ' B 510  VAL HG12', -0.446, (147.571, 144.081, 182.221)), (' C1309  NAG  H3 ', ' C1309  NAG  H83', -0.445, (108.8, 103.736, 128.48)), (' A1309  NAG  H3 ', ' A1309  NAG  H83', -0.445, (121.465, 175.149, 128.531)), (' B 761  ARG  NE ', ' C 953  GLN  OE1', -0.444, (119.83, 138.683, 130.133)), (' A 280  ASN  ND2', ' A 284  THR  OG1', -0.444, (170.514, 160.607, 138.83)), (' C 403  ARG  HG2', ' C 495  TYR  CE2', -0.443, (146.568, 123.556, 188.504)), (' B1309  NAG  H3 ', ' B1309  NAG  H83', -0.443, (176.643, 128.458, 128.358)), (' B 454  ARG  NH2', ' B 469  SER  O  ', -0.441, (142.343, 165.89, 181.941)), (' C 280  ASN  ND2', ' C 284  THR  OG1', -0.44, (96.818, 153.821, 138.434)), (' C 138  ASP  N  ', ' C 138  ASP  OD2', -0.439, (74.678, 133.663, 171.355)), (' B 133  PHE  HB3', ' B 135  PHE  CE1', -0.437, (157.88, 88.61, 175.227)), (' A 138  ASP  N  ', ' A 138  ASP  OD2', -0.436, (164.568, 189.766, 171.034)), (' C 118  LEU  CD2', ' C 120  VAL HG23', -0.436, (83.301, 145.749, 169.309)), (' A 454  ARG  HG3', ' A 491  PRO  HB2', -0.436, (110.501, 123.922, 183.351)), (' A 358  ILE  HB ', ' A 395  VAL HG13', -0.435, (111.814, 151.531, 172.841)), (' B 358  ILE  HB ', ' B 395  VAL HG13', -0.434, (161.327, 148.676, 172.894)), (' B 394  ASN  N  ', ' B 516  GLU  OE2', -0.432, (160.642, 150.598, 165.639)), (' C 420  ASP  OD1', ' C 421  TYR  N  ', -0.432, (153.485, 123.825, 177.112)), (' C 358  ILE  HB ', ' C 395  VAL HG13', -0.432, (134.342, 106.916, 173.215)), (' B 118  LEU  CD2', ' B 120  VAL HG23', -0.431, (153.14, 85.455, 169.281)), (' A 118  LEU  CD2', ' A 120  VAL HG23', -0.43, (170.557, 176.448, 169.297)), (' A 517  LEU HD11', ' C 975  ASP  OD2', -0.429, (120.235, 150.721, 158.316)), (' C 133  PHE  HB3', ' C 135  PHE  CE1', -0.429, (84.025, 140.22, 175.507)), (' A 557  LYS  NZ ', ' A 574  ASP  OD2', -0.429, (110.44, 159.894, 142.126)), (' A1125  VAL HG23', ' C 913  TYR  HB3', -0.428, (119.052, 148.92, 74.957)), (' B 420  ASP  OD1', ' B 421  TYR  N  ', -0.428, (137.253, 157.119, 176.91)), (' C 393  THR  OG1', ' C 516  GLU  OE2', -0.426, (136.77, 106.923, 164.294)), (' C 454  ARG  HG3', ' C 491  PRO  HB2', -0.424, (158.448, 119.739, 183.032)), (' B 454  ARG  HG3', ' B 491  PRO  HB2', -0.423, (138.298, 163.487, 182.985)), (' A 133  PHE  HB3', ' A 135  PHE  CE1', -0.423, (165.393, 178.65, 175.071)), (' A 589  PRO  HD2', ' C 851  PHE  CD2', -0.421, (120.515, 161.202, 140.705)), (' C 557  LYS  NZ ', ' C 574  ASP  OD2', -0.42, (127.597, 101.919, 142.272)), (' A 420  ASP  OD1', ' A 421  TYR  N  ', -0.42, (116.888, 126.196, 177.067)), (' A 349  SER  OG ', ' A 452  LEU  O  ', -0.418, (112.043, 133.119, 186.748)), (' C 118  LEU HD21', ' C 120  VAL HG23', -0.414, (83.105, 145.501, 169.803)), (' B 349  SER  OG ', ' B 452  LEU  O  ', -0.413, (144.834, 157.901, 186.829)), (' B 377  PHE  CD1', ' B 434  ILE HD12', -0.413, (153.682, 139.236, 177.758)), (' A 454  ARG  NH2', ' A 469  SER  O  ', -0.412, (106.515, 126.437, 182.029)), (' C 377  PHE  CD1', ' C 434  ILE HD12', -0.412, (129.798, 118.593, 177.822)), (' A 118  LEU HD21', ' A 120  VAL HG23', -0.41, (170.616, 176.568, 169.353)), (' B 913  TYR  HB3', ' C1125  VAL HG23', -0.41, (132.777, 114.762, 75.106)), (' C 349  SER  OG ', ' C 452  LEU  O  ', -0.41, (150.086, 116.566, 186.916)), (' A 807  LYS  O  ', ' A 810  LYS  NZ ', -0.409, (173.831, 136.405, 105.707)), (' A 381  GLY  O  ', ' C 979  ARG  NH1', -0.406, (123.191, 147.029, 162.917)), (' B 557  LYS  NZ ', ' B 574  ASP  OD2', -0.405, (169.149, 145.6, 142.381)), (' A 377  PHE  CD1', ' A 434  ILE HD12', -0.405, (123.92, 149.55, 177.796)), (' B 118  LEU HD21', ' B 120  VAL HG23', -0.404, (153.53, 85.47, 169.767)), (' C 366  SER  O  ', ' C 370  ASN  ND2', -0.404, (120.491, 115.016, 178.42)), (' B 600  PRO  HD3', ' B 688  ILE HD11', -0.403, (160.129, 108.904, 122.495)), (' C 600  PRO  HD3', ' C 688  ILE HD11', -0.402, (100.057, 127.807, 122.349)), (' A 900  TYR  HE1', ' B1103  ARG  HE ', -0.401, (148.387, 133.488, 80.023)), (' A 366  SER  O  ', ' A 370  ASN  ND2', -0.4, (125.487, 159.484, 178.347)), (' A 600  PRO  HD3', ' A 688  ILE HD11', -0.4, (146.82, 170.779, 122.416)), (' B 438  SER  OG ', ' B 509  ARG  HG3', -0.4, (150.7, 145.837, 189.159))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
