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
data['rama'] = [('A', ' 321 ', 'GLN', 0.08590283711349223, (216.653, 205.78899999999996, 174.222))]
data['omega'] = [('A', ' 527 ', 'PRO', None, (198.90600000000003, 203.4, 198.221)), ('D', ' 146 ', 'PRO', None, (202.28500000000008, 231.339, 271.728))]
data['rota'] = [('D', ' 432 ', 'ASN', 0.005944755286222892, (234.01200000000014, 245.175, 254.29400000000007)), ('D', ' 474 ', 'MET', 0.08550842086391404, (220.9550000000001, 217.21900000000002, 287.341)), ('D', ' 540 ', 'HIS', 0.13324083542543633, (231.50600000000017, 233.89999999999995, 251.89700000000005)), ('A', ' 312 ', 'ILE', 0.023044834837316938, (239.13100000000006, 200.66699999999997, 177.02400000000006)), ('A', ' 316 ', 'SER', 0.26901810400265347, (226.007, 199.57799999999997, 177.47900000000004)), ('A', ' 318 ', 'PHE', 0.20016150483750123, (222.092, 198.82199999999997, 171.993)), ('A', ' 336 ', 'CYS', 0.10952435675287374, (192.251, 199.402, 205.13)), ('A', ' 358 ', 'ILE', 0.0, (194.61600000000007, 193.26499999999996, 207.328)), ('A', ' 546 ', 'LEU', 0.0311516026004303, (209.80400000000003, 196.16500000000002, 191.536)), ('A', ' 563 ', 'GLN', 0.2974489648380686, (204.66300000000004, 181.95, 192.20200000000006)), ('A', ' 590 ', 'CYS', 0.2119244146243981, (216.64600000000004, 197.33800000000002, 175.364)), ('A', ' 591 ', 'SER', 0.037865878042591276, (218.61800000000005, 194.98500000000004, 173.029)), ('A', ' 592 ', 'PHE', 0.02684179489874898, (221.097, 192.059, 173.48500000000004))]
data['cbeta'] = []
data['probe'] = [(' A 559  PHE  CE2', ' A 584  ILE HD12', -1.006, (206.384, 182.374, 183.551)), (' A 559  PHE  CE2', ' A 584  ILE  CD1', -0.82, (206.307, 182.761, 182.959)), (' A 559  PHE  HE2', ' A 584  ILE HD12', -0.769, (205.988, 183.349, 183.971)), (' A  67  ALA  O  ', ' A 262  ALA  HA ', -0.729, (214.63, 237.033, 152.829)), (' A 559  PHE  HE2', ' A 584  ILE  CD1', -0.72, (206.07, 183.799, 183.877)), (' A 362  VAL HG23', ' A 526  GLY  HA3', -0.639, (197.402, 200.65, 197.372)), (' A 546  LEU  CD2', ' A 565  PHE  CE2', -0.61, (208.018, 191.872, 189.529)), (' D 168  TRP  HE1', ' D 502  SER  HB3', -0.602, (211.356, 222.94, 278.595)), (' A 592  PHE  H  ', ' A 634  ARG  NH2', -0.588, (219.99, 193.245, 171.526)), (' A 393  THR  O  ', ' A 523  THR  OG1', -0.565, (199.101, 190.228, 201.618)), (' D 269  ASP  OD1', ' D 270  MET  N  ', -0.559, (214.863, 230.281, 273.516)), (' D  85  LEU  O  ', ' D  94  LYS  NZ ', -0.553, (224.719, 188.034, 254.222)), (' D 247  LYS  HB3', ' D 282  THR HG22', -0.544, (227.64, 242.0, 272.387)), (' D 261  CYS  HB2', ' D 488  VAL HG13', -0.532, (228.583, 230.362, 283.424)), (' D  32  PHE  CD1', ' D  76  GLN  HG2', -0.527, (206.773, 193.341, 251.378)), (' A 329  PHE  HE2', ' A 528  LYS  HD3', -0.507, (203.311, 202.74, 192.352)), (' A 589  PRO  O  ', ' A 590  CYS  C  ', -0.507, (216.764, 195.458, 174.566)), (' D 402  GLU  HB3', ' D 518  ARG  HD3', -0.502, (220.346, 220.501, 257.719)), (' A 546  LEU HD23', ' A 565  PHE  CE2', -0.502, (207.778, 192.118, 190.026)), (' A 457  ARG  NH1', ' A 467  ASP  OD1', -0.501, (204.018, 181.229, 229.688)), (' A  21  ARG  NH1', ' A  79  PHE  O  ', -0.495, (205.064, 232.018, 151.374)), (' A  96  GLU  OE2', ' A 101  ILE  N  ', -0.494, (210.87, 238.382, 161.797)), (' A 641  ASN  HB3', ' A 653  ALA  O  ', -0.488, (240.075, 199.147, 160.89)), (' A 503  VAL  HA ', ' A 506  GLN HE21', -0.475, (202.885, 210.941, 232.678)), (' D 204  ARG  HD2', ' D 219  ARG  O  ', -0.473, (228.478, 204.613, 268.124)), (' D 187  LYS  HB3', ' D 199  TYR  CD2', -0.468, (215.569, 203.937, 273.782)), (' D 320  LEU  HB3', ' D 321  PRO  HD2', -0.467, (218.794, 218.368, 237.487)), (' D 177  ARG  HB3', ' D 178  PRO  HD3', -0.466, (209.895, 213.832, 287.803)), (' D 457  GLU  HG2', ' D 513  ILE  HB ', -0.463, (223.948, 213.159, 268.198)), (' A 246  ARG  NH2', ' A 254  SER  O  ', -0.459, (199.217, 241.672, 148.508)), (' D 284  PRO  HB3', ' D 594  TRP  CH2', -0.458, (232.103, 243.565, 265.143)), (' A 292  ALA  CB ', ' A 321  GLN HE22', -0.457, (220.304, 207.798, 174.588)), (' D 476  LYS  O  ', ' D 480  MET  HG2', -0.456, (227.445, 217.495, 282.846)), (' A 320  VAL  O  ', ' A 320  VAL HG12', -0.456, (214.616, 203.244, 171.884)), (' A 594  GLY  O  ', ' A 612  TYR  HA ', -0.45, (230.157, 194.407, 171.57)), (' A 418  ILE HD13', ' A 422  ASN HD22', -0.447, (205.299, 192.813, 230.711)), (' A  29  THR HG23', ' A  62  VAL HG23', -0.447, (219.252, 223.41, 160.16)), (' A 108  THR HG22', ' A 109  THR HG23', -0.446, (192.368, 219.905, 164.772)), (' A 421  TYR  CD1', ' A 457  ARG  HB3', -0.446, (208.999, 185.269, 232.064)), (' D 439  LEU  HA ', ' D 439  LEU HD23', -0.444, (228.746, 235.928, 257.913)), (' A 592  PHE  H  ', ' A 634  ARG HH21', -0.443, (220.925, 192.994, 171.271)), (' A 319  ARG  HA ', ' A 319  ARG  HD3', -0.442, (219.59, 201.366, 174.311)), (' A 321  GLN  HA ', ' A 321  GLN  NE2', -0.442, (217.87, 206.651, 174.366)), (' D 291  ILE  O  ', ' D 291  ILE HG13', -0.437, (219.675, 241.497, 251.734)), (' D 398  GLU  HG3', ' D 514  ARG  HG2', -0.436, (220.996, 212.428, 261.253)), (' D  93  VAL HG12', ' D  97  LEU HD12', -0.435, (218.702, 190.382, 249.899)), (' D 455  MET  HB3', ' D 455  MET  HE3', -0.435, (225.33, 220.811, 275.294)), (' A 500  THR  OG1', ' D  41  TYR  OH ', -0.431, (198.474, 211.081, 241.846)), (' D 315  PHE  HA ', ' D 318  VAL HG12', -0.431, (220.524, 224.71, 239.195)), (' A  29  THR  OG1', ' A  30  ASN  N  ', -0.43, (222.367, 222.406, 159.63)), (' D 308  PHE  CZ ', ' D 333  LEU HD22', -0.428, (206.294, 227.712, 246.239)), (' A 185  ASN  HB2', ' A 212  LEU  O  ', -0.428, (224.912, 238.287, 157.679)), (' A 341  VAL HG23', ' A 356  LYS  HZ2', -0.428, (193.099, 197.053, 212.101)), (' A 115  GLN HE22', ' A 167  THR HG23', -0.426, (188.719, 229.477, 175.487)), (' D 336  PRO  HG2', ' D 340  GLN  O  ', -0.426, (192.607, 227.251, 253.002)), (' A 431  GLY  HA3', ' A 513  LEU  O  ', -0.424, (206.088, 196.453, 211.844)), (' A 206  LYS  HB3', ' A 223  LEU HD22', -0.417, (218.577, 231.525, 174.305)), (' D 524  GLN  HG2', ' D 583  PRO  HG2', -0.417, (235.059, 220.838, 254.399)), (' A 100  ILE HD11', ' A 245  HIS  HE1', -0.417, (211.356, 242.891, 156.009)), (' D 482  ARG HH21', ' D 489  GLU  CD ', -0.416, (225.045, 226.207, 288.22)), (' A 642  VAL HG22', ' A 651  ILE HG12', -0.416, (233.347, 197.26, 161.85)), (' A 102  ARG  HD2', ' A 121  ASN  O  ', -0.415, (204.833, 241.64, 165.044)), (' A 105  ILE HD11', ' A 239  GLN HE21', -0.414, (198.616, 229.514, 160.864)), (' D 230  PHE  HA ', ' D 233  ILE HG22', -0.414, (234.643, 221.443, 267.588)), (' A 409  GLN  OE1', ' A 418  ILE  HB ', -0.412, (209.419, 195.903, 229.114)), (' D 209  VAL HG11', ' D 565  PRO  HB3', -0.41, (230.021, 201.907, 253.401)), (' D 403  ALA  O  ', ' D 407  ILE HG23', -0.409, (224.307, 222.221, 251.471)), (' D  96  GLN  HG2', ' D 391  LEU  HB2', -0.409, (215.396, 198.199, 249.602)), (' A 355  ARG  NH2', ' A 398  ASP  OD2', -0.408, (201.809, 190.793, 215.966)), (' D 529  LEU HD21', ' D 554  LEU HD22', -0.407, (226.679, 220.877, 244.625)), (' A 382  VAL HG11', ' A 387  LEU  HB3', -0.407, (207.725, 200.683, 204.947)), (' A  33  THR  HA ', ' A  58  PHE  CD2', -0.406, (224.163, 219.946, 171.164)), (' A 200  TYR  HB3', ' A 228  ASP  OD1', -0.403, (203.217, 225.913, 181.777)), (' D 215  TYR  HE2', ' D 568  LEU HD13', -0.402, (233.722, 204.443, 247.443)), (' A  44  ARG  O  ', ' A 283  GLY  HA2', -0.4, (225.78, 227.953, 188.922))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
