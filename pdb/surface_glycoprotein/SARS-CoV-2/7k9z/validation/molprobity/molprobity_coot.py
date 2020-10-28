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
data['rama'] = [('B', ' 101 ', 'GLY', 0.030417336832994385, (-20.89599999999999, -35.10700000000001, 21.389)), ('B', ' 127 ', 'SER', 0.0153835398461147, (5.534000000000005, -43.95099999999999, -21.218)), ('B', ' 128 ', 'SER', 0.014738192025805561, (4.956000000000016, -47.72899999999999, -21.348))]
data['omega'] = [('A', '   8 ', 'PRO', None, (-15.612999999999992, -58.321, 13.627000000000004)), ('A', '  95 ', 'PRO', None, (-10.21199999999999, -46.66700000000001, 34.427)), ('B', ' 147 ', 'PRO', None, (8.994000000000003, -32.23, 9.147000000000002)), ('B', ' 149 ', 'PRO', None, (2.7049999999999987, -32.717, 8.307)), ('L', '   8 ', 'PRO', None, (-28.103999999999996, -34.985, 78.383)), ('L', '  95 ', 'PRO', None, (-30.943999999999992, -21.293999999999993, 58.34300000000001))]
data['rota'] = [('H', ' 121 ', 'VAL', 0.0668940649320185, (-1.8880000000000006, -6.568, 90.92500000000001)), ('L', '  89 ', 'GLN', 0.04382735044861763, (-25.827, -29.741999999999994, 64.369)), ('L', '  90 ', 'GLN', 0.038561859089316135, (-28.41899999999999, -29.959999999999994, 61.618000000000016)), ('L', ' 129 ', 'THR', 0.008159601566148922, (-11.824, 0.45499999999999996, 95.279)), ('L', ' 146 ', 'VAL', 0.19045026739724402, (-21.766999999999996, -18.538, 95.765)), ('L', ' 154 ', 'LEU', 0.039726670875493086, (-28.726999999999997, -11.027, 100.23800000000001)), ('L', ' 158 ', 'ASN', 0.020240144138212388, (-22.507999999999996, -8.08, 91.123)), ('L', ' 171 ', 'SER', 0.1037109997397975, (-10.256000000000002, -33.953, 89.26300000000003)), ('A', '  27B', 'VAL', 0.21614528404366576, (-21.405999999999988, -52.941, 31.727)), ('A', '  27D', 'TYR', 0.10931215434842295, (-25.151000000000003, -51.281, 36.907000000000004)), ('A', '  47 ', 'LEU', 0.29180914829847315, (-23.468999999999998, -41.735, 17.534)), ('A', ' 187 ', 'GLU', 0.005899918629049646, (24.232000000000014, -48.694, -12.25)), ('A', ' 214 ', 'CYS', 0.2436558644380228, (13.538000000000006, -43.332, -21.735000000000003)), ('B', ' 129 ', 'LYS', 0.0, (1.4570000000000138, -47.404999999999994, -19.933)), ('B', ' 163 ', 'VAL', 0.004224941792146306, (-5.6139999999999946, -38.184999999999995, -8.703)), ('B', ' 198 ', 'VAL', 0.14346389623234182, (3.828000000000003, -29.737, -3.205000000000001)), ('B', ' 216 ', 'CYS', 0.057420998870256826, (9.118000000000011, -43.680000000000014, -25.65)), ('E', ' 350 ', 'VAL', 0.11771100488323712, (-34.246000000000016, -25.361, 44.957)), ('E', ' 357 ', 'ARG', 0.0009512222615918473, (-44.198, -21.185, 59.267)), ('E', ' 362 ', 'VAL', 0.26663126717201624, (-56.04, -14.304000000000004, 59.027)), ('E', ' 395 ', 'VAL', 0.2442083731667685, (-49.518, -23.51, 56.849)), ('E', ' 430 ', 'THR', 0.13375023024460908, (-53.28099999999999, -30.582, 50.16900000000001)), ('E', ' 444 ', 'LYS', 0.06069120594835627, (-28.920999999999996, -9.11, 35.316)), ('E', ' 510 ', 'VAL', 0.24877810647982243, (-42.432, -20.10000000000001, 42.866))]
data['cbeta'] = []
data['probe'] = [(' E 469  SER  HA ', ' H  97  GLY  HA3', -0.812, (-24.142, -31.158, 50.634)), (' L 148  TRP  HB3', ' L 179  LEU HD12', -0.785, (-21.745, -10.073, 97.252)), (' L 190  LYS  HD2', ' L 211  ARG  HA ', -0.772, (-14.071, -3.095, 107.856)), (' B 126  PRO  HD2', ' B 213  PRO  HA ', -0.725, (5.863, -38.215, -20.173)), (' A  35  TRP  HB2', ' A  48  ILE  HB ', -0.708, (-23.311, -45.928, 18.95)), (' L  36  TYR  HE1', ' L  89  GLN  HG2', -0.684, (-22.192, -30.735, 62.935)), (' B 130  SER  HG ', ' B 135  THR  N  ', -0.672, (-4.32, -45.0, -21.852)), (' B 121  VAL HG22', ' B 142  VAL HG12', -0.658, (8.263, -32.848, -4.005)), (' B 126  PRO  HA ', ' B 129  LYS  HE2', -0.654, (4.416, -42.841, -18.444)), (' L  33  LEU  HB3', ' L  51  ALA  HB2', -0.653, (-28.217, -36.646, 62.565)), (' A  54  ARG  NH2', ' A  60  ASP  OD1', -0.648, (-32.981, -42.742, 14.097)), (' H 138  LEU HD13', ' H 211  VAL HG21', -0.646, (0.867, -15.11, 98.644)), (' E 382  VAL HG11', ' E 387  LEU HD13', -0.643, (-57.866, -24.0, 50.375)), (' L 142  ARG HH21', ' L 163  VAL HG21', -0.609, (-18.0, -21.92, 87.457)), (' H 181  VAL HG11', ' L 135  LEU HD22', -0.605, (-8.667, -18.07, 95.581)), (' A 135  LEU HD11', ' B 181  VAL HG21', -0.602, (-0.783, -43.595, -9.536)), (' B 126  PRO  HG3', ' B 138  LEU  HB3', -0.602, (2.452, -39.375, -16.919)), (' L 136  LEU HD21', ' L 196  VAL HG21', -0.594, (-17.676, -21.55, 98.494)), (' L 121  SER  OG ', ' L 124  GLN  OE1', -0.592, (-4.103, -4.22, 97.785)), (' A 113  PRO  HD2', ' A 201  LEU HD13', -0.584, (-4.965, -57.361, -11.593)), (' E 439  ASN  O  ', ' E 443  SER  OG ', -0.583, (-34.26, -11.057, 34.486)), (' B 148  GLU  HG2', ' B 149  PRO  HA ', -0.582, (2.295, -34.762, 6.568)), (' A 116  PHE  CD1', ' B 129  LYS  HG2', -0.573, (0.719, -46.752, -17.107)), (' B 127  SER  H  ', ' B 129  LYS  HE2', -0.571, (4.28, -44.199, -18.632)), (' H  24  ALA  HB1', ' H  27  TYR  HE1', -0.569, (-8.532, -26.32, 51.584)), (' B 195  ILE HG22', ' B 210  LYS  HA ', -0.569, (4.974, -28.905, -14.504)), (' E 454  ARG  NH1', ' E 469  SER  O  ', -0.566, (-25.509, -32.522, 46.8)), (' L  24  ARG  NE ', ' L  70  ASP  OD1', -0.566, (-37.437, -35.54, 69.174)), (' A  33  LEU  HB3', ' A  51  ALA  HB2', -0.565, (-23.41, -49.796, 25.355)), (' E 439  ASN  HB2', ' E 506  GLN HE21', -0.564, (-37.801, -12.705, 32.003)), (' B  87  THR HG23', ' B 110  THR  HA ', -0.561, (4.888, -37.028, 16.236)), (' L 189  HIS  CE1', ' L 191  VAL  HB ', -0.557, (-21.252, -6.144, 108.544)), (' E 418  ILE HD13', ' E 422  ASN HD22', -0.557, (-33.859, -29.388, 40.111)), (' L 186  TYR  O  ', ' L 192  TYR  OH ', -0.547, (-17.385, -1.551, 103.434)), (' H  96  ARG  NH1', ' H  98  ASP  OD1', -0.544, (-22.757, -34.313, 53.466)), (' A  65  SER  HG ', ' A  72  THR  HG1', -0.542, (-27.123, -54.967, 18.444)), (' A 116  PHE  HD2', ' A 135  LEU HD22', -0.54, (-0.764, -46.891, -12.576)), (' B 123  PRO  HD3', ' B 209  LYS  HE2', -0.539, (11.608, -32.685, -11.539)), (' L  22  THR HG22', ' L  72  THR HG22', -0.533, (-30.606, -39.678, 72.664)), (' H  85  GLU  N  ', ' H  85  GLU  OE1', -0.532, (-22.048, -6.38, 71.68)), (' L  82  ASP  O  ', ' L  86  TYR  OH ', -0.526, (-15.395, -37.579, 74.766)), (' A 136  LEU HD11', ' A 146  VAL HG11', -0.525, (2.037, -54.438, -7.25)), (' B   2  VAL  N  ', ' B  25  SER  O  ', -0.521, (-18.897, -23.652, 21.672)), (' A  80  ALA  HA ', ' A 106  ILE HD11', -0.518, (-19.824, -45.944, 0.521)), (' B 168  ALA  HB2', ' B 178  LEU HD23', -0.518, (3.875, -38.522, 2.364)), (' L 163  VAL HG22', ' L 175  LEU  HG ', -0.518, (-16.696, -20.97, 89.58)), (' H 146  PHE  N  ', ' H 175  LEU HD23', -0.515, (-6.552, -3.555, 79.967)), (' A  14  SER  HB2', ' A  17  GLU  HG3', -0.508, (-24.225, -55.618, 0.033)), (' E 353  TRP  HZ3', ' E 355  ARG HH11', -0.504, (-40.597, -27.067, 52.845)), (' B  11  VAL HG11', ' B 147  PRO  HG3', -0.503, (7.542, -31.47, 12.709)), (' A  42  GLN  HB2', ' A  43  PRO  HD2', -0.5, (-11.492, -33.996, 12.7)), (' L 113  PRO  HB2', ' L 136  LEU HD22', -0.499, (-16.114, -24.653, 97.95)), (' A 142  ARG  HE ', ' A 163  VAL HG21', -0.498, (-2.697, -51.977, 0.874)), (' E 401  VAL HG22', ' E 509  ARG  HG2', -0.497, (-37.895, -16.744, 42.426)), (' B  63  PHE  O  ', ' B  67  VAL HG12', -0.496, (0.502, -38.542, 33.169)), (' H  28  THR  O  ', ' H  31  SER  OG ', -0.493, (-11.927, -29.947, 46.245)), (' L 106  ILE HD11', ' L 171  SER  OG ', -0.491, (-10.061, -36.852, 87.555)), (' H  60  ALA  HB3', ' H  63  PHE  CD1', -0.49, (-25.733, -14.382, 60.874)), (' B  70  THR  HB ', ' B  79  TYR  HB2', -0.488, (-2.636, -26.293, 31.211)), (' A 145  LYS  HG3', ' A 197  THR  HB ', -0.485, (1.21, -61.157, -5.221)), (' H 195  ILE HG12', ' H 210  LYS  HG3', -0.484, (6.887, -11.088, 98.004)), (' H  60  ALA  HB3', ' H  63  PHE  HD1', -0.484, (-26.041, -14.636, 60.556)), (' A 120  PRO  HD3', ' A 132  VAL HG22', -0.482, (14.163, -47.156, -10.766)), (' E 334  ASN  N  ', ' E 334  ASN  OD1', -0.479, (-54.059, -10.761, 64.08)), (' A 108  ARG  HD2', ' A 171  SER  HB2', -0.477, (-15.839, -50.42, -5.524)), (' H 146  PHE  HB3', ' H 147  PRO  HD3', -0.476, (-5.36, -3.683, 77.25)), (' H 119  PRO  HB3', ' H 145  TYR  HB3', -0.475, (-3.634, -6.333, 83.536)), (' L 133  VAL HG22', ' L 178  THR HG22', -0.474, (-12.362, -11.193, 93.911)), (' H  96  ARG HH11', ' H  99  THR HG22', -0.472, (-20.657, -33.886, 54.325)), (' L   2  ILE HD11', ' L  25  ALA  HB1', -0.472, (-34.329, -30.138, 63.747)), (' B 168  ALA  HA ', ' B 178  LEU  HB3', -0.468, (4.178, -40.626, 1.493)), (' B  33  GLY  HA3', ' B  50  TRP  HE1', -0.467, (-15.189, -33.649, 32.988)), (' B  54  SER  HB3', ' H  53  MET  SD ', -0.467, (-15.479, -26.5, 40.119)), (' E 466  ARG  HD2', ' L  92  ASN  O  ', -0.467, (-32.444, -28.459, 53.771)), (' A   3  VAL HG12', ' A  26  SER  HB2', -0.467, (-11.359, -57.078, 29.136)), (' B  68  THR  HB ', ' B  81  GLU  HB2', -0.467, (2.144, -30.974, 32.415)), (' A 144  ALA  HB2', ' A 198  HIS  HD2', -0.466, (-3.896, -56.946, -5.125)), (' E 440  ASN  N  ', ' E 440  ASN  OD1', -0.465, (-37.394, -9.376, 36.303)), (' L  89  GLN  HB2', ' L  89  GLN HE21', -0.463, (-25.002, -27.631, 62.818)), (' L 141  PRO  HD2', ' L 198  HIS  CE1', -0.462, (-19.16, -30.615, 94.934)), (' L 138  ASN  HA ', ' L 172  THR  HB ', -0.459, (-11.45, -30.002, 93.826)), (' E 457  ARG  NH1', ' E 467  ASP  OD2', -0.457, (-30.131, -36.167, 49.213)), (' B  80  MET  HE1', ' B  82  LEU  HB2', -0.456, (1.265, -35.163, 27.178)), (' H  62  LYS  HA ', ' H  62  LYS  HD2', -0.455, (-30.018, -9.826, 59.743)), (' E 406  GLU  HB3', ' E 418  ILE HG13', -0.452, (-37.365, -27.972, 37.478)), (' L 113  PRO  HB3', ' L 139  PHE  HB3', -0.448, (-16.164, -27.19, 96.705)), (' H 159  LEU HD21', ' H 182  VAL HG21', -0.448, (2.0, -21.31, 96.075)), (' L   6  GLN  HG3', ' L 100  PRO  HD2', -0.442, (-28.136, -29.043, 72.457)), (' E 470  THR  H  ', ' H  97  GLY  HA3', -0.442, (-23.198, -30.731, 50.82)), (' L  37  GLN  HB2', ' L  47  LEU HD11', -0.441, (-16.914, -35.521, 69.963)), (' A  14  SER  OG ', ' A 107  LYS  HD2', -0.439, (-20.593, -57.01, -0.972)), (' L 124  GLN  O  ', ' L 128  GLY  N  ', -0.439, (-7.757, 2.296, 94.637)), (' E 439  ASN  HA ', ' E 507  PRO  HG2', -0.437, (-35.703, -13.864, 35.302)), (' H  84  SER  O  ', ' H  87  THR HG22', -0.434, (-18.296, -8.627, 72.405)), (' H 178  LEU HD12', ' H 179  SER  H  ', -0.434, (-7.908, -14.765, 87.804)), (' B  41  PRO  HD3', ' B  88  ALA  HA ', -0.432, (0.533, -40.779, 16.524)), (' A 187  GLU  HA ', ' A 211  ARG  HE ', -0.431, (22.665, -48.127, -13.561)), (' H 153  SER  OG ', ' H 197  ASN  HB2', -0.43, (6.513, -15.302, 88.332)), (' H  12  LYS  HB2', ' H 111  VAL HG22', -0.429, (-12.913, -5.243, 66.766)), (' A  36  TYR  OH ', ' B  96  PRO  HG3', -0.429, (-18.317, -40.725, 24.146)), (' H 163  VAL HG12', ' H 182  VAL  HB ', -0.429, (-0.256, -21.182, 94.492)), (' B  40  ALA  HB3', ' B  43  GLN  HB2', -0.426, (-1.74, -46.104, 17.808)), (' E 342  PHE  HE1', ' E 511  VAL  HB ', -0.426, (-45.551, -18.162, 46.899)), (' B 154  TRP  CZ3', ' B 196  CYS  HB3', -0.425, (2.298, -33.329, -9.971)), (' A 118  PHE  CE2', ' B 129  LYS  HE3', -0.424, (4.314, -43.676, -15.367)), (' B 119  PRO  HB3', ' B 145  TYR  HB3', -0.423, (9.905, -33.579, 1.746)), (' E 418  ILE  HA ', ' E 422  ASN  HB2', -0.423, (-35.312, -30.301, 41.646)), (' E 473  TYR  O  ', ' E 488  CYS  HA ', -0.421, (-19.209, -38.705, 41.039)), (' A  35  TRP  CZ3', ' A  88  CYS  HB3', -0.421, (-18.625, -50.812, 19.258)), (' L 182  SER  O  ', ' L 186  TYR  N  ', -0.42, (-17.346, 0.713, 99.778)), (' A 214  CYS  O  ', ' B 214  LYS  HG2', -0.42, (11.616, -41.507, -20.25)), (' B  33  GLY  HA3', ' B  50  TRP  NE1', -0.419, (-14.729, -33.981, 33.038)), (' E 393  THR  HA ', ' E 522  ALA  HA ', -0.418, (-55.4, -24.525, 63.021)), (' A 147  GLN  HB2', ' A 154  LEU HD11', -0.418, (9.932, -60.797, -4.97)), (' L  46  LEU HD21', ' L  49  TYR  HB3', -0.417, (-19.316, -36.112, 59.113)), (' A 136  LEU HD13', ' A 175  LEU HD22', -0.415, (1.271, -52.299, -5.407)), (' B   9  ALA  HA ', ' B 107  THR HG23', -0.412, (-0.469, -29.349, 16.99)), (' A 124  GLN  HG2', ' A 130  ALA  HA ', -0.412, (16.92, -41.333, -7.366)), (' B 186  SER  HA ', ' B 189  LEU HD13', -0.412, (-2.108, -39.694, -22.805)), (' L  33  LEU  O  ', ' L  51  ALA  N  ', -0.411, (-25.305, -37.39, 61.353)), (' L  29  ILE  HA ', ' L  92  ASN  ND2', -0.411, (-34.319, -31.96, 57.657)), (' E 450  ASN  HA ', ' H  56  THR HG22', -0.409, (-24.939, -18.198, 42.804)), (' B 127  SER  OG ', ' B 128  SER  N  ', -0.409, (6.494, -45.917, -21.662)), (' L 105  ASP  N  ', ' L 105  ASP  OD1', -0.409, (-17.841, -34.512, 83.621)), (' E 439  ASN  CB ', ' E 506  GLN HE21', -0.406, (-37.46, -12.587, 32.407)), (' B   7  SER  O  ', ' B 107  THR  OG1', -0.405, (-3.886, -28.3, 18.634)), (' L   4  MET  HE1', ' L  25  ALA  HB2', -0.405, (-32.572, -31.547, 65.208)), (' E 339  GLY  O  ', ' E 343  ASN  HB2', -0.402, (-43.372, -8.854, 50.331)), (' A 105  GLU  OE1', ' A 173  TYR  OH ', -0.402, (-10.888, -51.655, 2.265)), (' L  78  LEU  HA ', ' L  78  LEU HD12', -0.402, (-15.53, -42.778, 76.591)), (' L  35  TRP  CE2', ' L  73  LEU  HB2', -0.401, (-24.753, -37.847, 68.702)), (' A 113  PRO  HB3', ' A 139  PHE  CD1', -0.401, (-5.064, -52.662, -7.995)), (' E 456  PHE  HB3', ' E 473  TYR  CG ', -0.401, (-24.781, -37.972, 41.359))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
