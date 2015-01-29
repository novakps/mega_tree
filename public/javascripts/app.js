/*global  */
Ext.require([
    'Ext.tree.*',
    'Ext.data.*',
    'Ext.form.*',
    'Ext.tip.*'
]);

Ext.onReady(function() {
  Ext.QuickTips.init();

  Ext.define('NodeModel', {
    extend: 'Ext.data.TreeModel',
    fields: [
      { name: '_id'},
      { name: 'text', mapping: 'name'},
      { name: 'children'}
    ],
    idProperty: '_id',
    proxy: {
      type: 'rest',
      url: 'data'
    }
  });

  var store  = Ext.create('Ext.data.TreeStore', {
    model: 'NodeModel',
    root: {
      text: 'root',
      _id: '0',
      expanded: true
    },
    buffered: true,
    folderSort: false,
    remoteFilter: true 
  });

  var tree = Ext.create('Ext.tree.Panel', {
    id: 'treePanel',
    store: store,
    title: 'Columns',
    width: 500,
    height: 800,
    rootVisible: false,
    renderTo: 'tree-div',
    useArrows: true,
      plugins: {
        ptype: 'bufferedrenderer'
      }
  });

  var input = Ext.create('Ext.form.field.Trigger', {
    triggerCls: 'x-form-clear-trigger',
    emptyText: 'search...',
    width: 500,
    border: 0,
    renderTo: 'filter-div',
    listeners: {
      change: function(field, newValue) {
        if (newValue.length) {
          store.filters.replace('0', store.decodeFilters({property: 'text', value: newValue})[0]);
        } else {
          store.clearFilter();
        }
        store.load();
      }
    },
    onTriggerClick: function() {
      input.setValue('');
    }
  });
  
});
