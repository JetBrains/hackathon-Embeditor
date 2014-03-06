import httplib
import socket
import xmlrpclib
from functools import wraps

import vim


IDEA_RPC_HOST = 'http://localhost'
IDEA_RPC_PORT = 63341


# Server proxy


def server():
    server_url = IDEA_RPC_HOST + ':' + str(IDEA_RPC_PORT)
    return xmlrpclib.ServerProxy(server_url).embeditor


def rpc(function):
    '''A decorator to protect functions using rpc from server errors.'''

    @wraps(function)
    def decorated_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except socket.error:
            show_error('IntelliJ server unavailable.')
        except xmlrpclib.Fault as e:
            show_error('IntelliJ server rpc fault: %d - %s.' % (e.faultCode,
                                                            e.faultString))
        except xmlrpclib.ProtocolError as e:
            show_error('IntelliJ server rpc protocol error: %d - %s.' %
                       (e.errcode, e.errmsg))
        except httplib.HTTPException as e:
            show_error('IntelliJ server http protocol error: %s.' % e.message)

    return decorated_function


# Main functionality (externally invocable)


@rpc
def resolve():
    file_path = current_file_path()
    row, col = get_caret_position()
    file_content = current_buffer_content()
    results = server().resolve(file_path, file_content, row, col)
    result_count = len(results)

    if result_count == 0:
        show_warning('No results.')
    elif result_count == 1:
        navigate_to_position(results[0])
    else:
        show_position_chooser(results)


@rpc
def complete(find_start, base_string):
    file_path = current_file_path()
    row, col = get_caret_position()
    file_content = (current_buffer_content_before_position(row, col) +
                    base_string +
                    current_buffer_content_after_position(row, col))

    server_method = ('getCompletionStartOffsetInLine' if find_start else
                     'getCompletionVariants')

    return getattr(server(), server_method)(file_path, file_content, row, col)

# Vim-interfacing functions


def current_file_path():
    return vim.eval('expand("%:p")')


def get_caret_position():
    # todo: col should consider tabwidth
    return to_standard_coordinates(*vim.current.window.cursor)


def set_caret_position(line, column):
    if line < len(vim.current.buffer):
        vim.current.window.cursor = to_vim_coordinates(line, 0)
        if column < len(vim.current.buffer[line]):
            vim.current.window.cursor = to_vim_coordinates(line, column)


def current_buffer_content():
    return '\n'.join(vim.current.buffer)


def current_buffer_content_before_position(row, col):
    first_lines = vim.current.buffer[:row]
    current_line_before_position = vim.current.buffer[row][:col]
    return '\n'.join(first_lines + [current_line_before_position])


def current_buffer_content_after_position(row, col):
    current_line_after_position = vim.current.buffer[row][col:]
    last_lines = vim.current.buffer[row + 1:]
    return '\n'.join([current_line_after_position] + last_lines)


def show_error(message):
    vim.command('redraw')
    vim.command('echohl ErrorMsg')
    vim.command('echomsg "%s"' % message)
    vim.command('echohl None')


def show_warning(message):
    vim.command('echohl WarningMsg')
    vim.command('echomsg "%s"' % message)
    vim.command('echohl None')


def navigate_to_position(position):
    if position['path'] != current_file_path():
        vim.command('edit %s' % position['path'])
    set_caret_position(position['line'], position['column'])


def show_position_chooser(positions):
    # use a location list; other approaches would be possible
    show_location_list(positions)


def show_location_list(locations):
    location_list_data = [{'filename': shorten_path(location['path']),
                           'lnum': to_vim_row(location['line']),
                           'col': to_vim_col(location['column']),
                           'text': location['text'].strip()}
                          for location in locations]

    # replace contents of current window's location list
    vim.Function('setloclist')(0, location_list_data, 'r')

    # show current window's location list window
    vim.command('lwindow')


def shorten_path(path):
    return vim.Function('fnamemodify')(path, ':~:.')


# Utility

def to_vim_row(row):
    return to_vim_coordinates(row, 0)[0]


def to_vim_col(col):
    return to_vim_coordinates(0, col)[1]


def to_vim_coordinates(row, col):
    '''Transform from standard coordinates to vim coordinates.'''
    return (row + 1, col)


def to_standard_coordinates(row, col):
    '''Transform from vim coordinates to standard coordinates.'''
    return (row - 1, col)
